const nodeRSA = require('node-rsa')

// 生成一个1024长度的密钥对
const key = new nodeRSA({ b: 1024 })
const publicKey = key.exportKey('pkcs8-public') // 公钥
const privateKey = key.exportKey('pkcs8-private') // 私钥
const txt = '123'

// 使用公钥加密
function encrypt(data) {
  const pubKey = new nodeRSA(publicKey, 'pkcs8-public')
  return pubKey.encrypt(Buffer.from(data), 'base64')
}

// 使用私钥解密
function decrypt(data) {
  const priKey = new nodeRSA(privateKey, 'pkcs8-private')
  return priKey.decrypt(Buffer.from(data, 'base64'), 'utf8')
}

const sign = encrypt(txt)
const _src = decrypt(sign)

console.log('加密：', sign)
console.log('解密：', _src)
/*
加密： fBaBFVPv+96I/r6a2tfPbYWa0yjgJKQ+K2/E9obGNo0dYBOSBzW2PgnPOHX+/pq0wUZPxJzcwt5YcMtOsUNuZAYpaPZJ9o6IOEKj823HBNbyerDMUfU3rINCk2FilRuxFpQPmBZTbSvSumKligdtsh1Vz02DwdRgbJHp5bm4Hjk=
解密： 123
*/

// 使用私钥对消息签名
function signRSA(data) {
  const priKey = new nodeRSA(privateKey, 'pkcs8-private')
  return priKey.sign(Buffer.from(data), 'hex')
}

// 使用公钥验证签名
function verifyRSA(decrypt, signs) {
  const pubKey = new nodeRSA(publicKey, 'pkcs8-public')
  return pubKey.verify(Buffer.from(decrypt), signs, 'utf8', 'hex')
}

const signature = signRSA(sign)

console.log('私钥签名：' + signature)
console.log('公钥验证：' + verifyRSA(sign, signature))

console.log("hello world");

const nodeRSA = require('node-rsa');
const crypto = require('crypto');



const publicKey = "-----BEGIN RSA PUBLIC KEY-----\n" +
"MEgCQQCVz3dxWapVRcebJnbF2xHTWNlsjpKXAHrU4/l3jtT81rP1GE/Z2HZMid33\n" +
"+JckD/yeBNauwLG44qolG1Csd42BAgMBAAE=\n" +
"-----END RSA PUBLIC KEY-----";

const encrypt = new nodeRSA({b: 512});
const password = document.getElementById('password');
const pub = encrypt.importKey(publicKey, 'pkcs1-public-pem');

const hash = crypto.createHash('md5');
// hash.update(password.value);
// console.log("creating hash");
// const digest = hash.digest('hex');
// console.log(digest);

// const encrypted_pw = pub.encrypt(digest, 'base64');
// console.log(encrypted_pw);

try {
    const register_btn = document.getElementById('register');
    if (register_btn != null) {
        console.log("register button found");
        register_btn.addEventListener('click', () => {
            hash.update(password.value);
            const digest = hash.digest('hex');

            password.value = digest;
            const username = document.getElementById('username');
            const rsa = new nodeRSA({b: 512});
            const public_key = rsa.exportKey('pkcs8-public');
            const private_key = rsa.exportKey('pkcs8-private');
            localStorage.setItem(username.value + '_public_key', public_key);
            localStorage.setItem(username.value + '_private_key', private_key);

            document.getElementById('pubKey').value = public_key;
            console.log("added public key to the server")
        });
    }
} catch (e) {
    console.log("register error");
}

try{
    const login_btn = document.getElementById('login');

    if (login_btn != null){
        console.log("login button found");
        login_btn.addEventListener('click', () => {
            hash.update(password.value);
            const digest = hash.digest('hex');

            password.value = digest;

            sessionStorage.setItem('username', document.getElementById('username').value);
        })
    }
}
catch(e){
    console.log("login error");
}

// const hash = crypto.createHash('md5');
// hash.update("1");
// const digest = hash.digest('base64');
// console.log(digest);




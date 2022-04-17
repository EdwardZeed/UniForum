const nodeRSA = require('node-rsa')



const friend = document.getElementById('friend')

const received_message_title = document.getElementById('received_message_title')
const received_message = document.getElementById('received_message')

const digital_signature = document.getElementById('ds')
if (received_message.innerHTML != ""){
    console.log("have message")
    const sender_public_key = document.getElementById('friend_public_key').innerHTML
    const digital_signature = document.getElementById('ds')
    const verify = new nodeRSA(sender_public_key)
    if (verify.verify(Buffer.from(received_message.innerHTML), digital_signature.value, 'utf8', 'hex')){
        console.log('verify success')
        const current_user_private_key = localStorage.getItem(sessionStorage.getItem('username')+'_private_key')
        const decrypt = new nodeRSA(current_user_private_key)
        const decrypt_msg = decrypt.decrypt(received_message.innerHTML, 'utf8')
        received_message.innerHTML = decrypt_msg
    }
    else{
        console.log('verify fail')
    }
}
else{
    received_message_title.setAttribute('hidden', 'true')
    received_message.setAttribute('hidden', 'true')
}
console.log(friend.innerHTML)

const friend_public_key = document.getElementById('friend_public_key')

try{
    const send_btn = document.getElementById('send')
    if (send_btn != null){
        send_btn.addEventListener('click', () => {
            const msg = document.getElementById('msg')
            console.log(friend_public_key.innerHTML)
            const encrypt = new nodeRSA(friend_public_key.innerHTML, 'pkcs8-public')
            const encrypt_msg = encrypt.encrypt(msg.value, 'base64')
            msg.value = encrypt_msg

            const current_user = sessionStorage.getItem('username')
            const current_user_private_key = localStorage.getItem(current_user+'_private_key')

            const signature = new nodeRSA(current_user_private_key)
            const sign = signature.sign(Buffer.from(encrypt_msg), 'hex')
            document.getElementById('ds').value = sign
            document.getElementById('sender').value = current_user

        })
    }
}
catch(err){
    console.log("message send error")
}


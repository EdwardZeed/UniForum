const rsa = require('node-rsa');

const privateKey = "-----BEGIN PRIVATE KEY-----\n" +
    "MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAhWn72iJjI1g63enW\n" +
    "rQiQ89ZxcYCa45HBKxL2KyQ6yZfOCgsIFhJREpA3U69hMYmiPAba1Cc8sddq2Wdz\n" +
    "/9Kv4wIDAQABAkBcl42/epYrdZSFZ0Eingtb77yT9ZmJzyKtbl+C2YYjWjZz0wao\n" +
    "xhtuz+in0vb+2JL1XVOXGPLbfO0H0/NenLNhAiEA/h753m25WjcyqsdVv6Dq2rJw\n" +
    "k90xRfiRjmOik8aFtP0CIQCGZoWzX46uHGNK/Z4C0Ar9wueRWLvHMgk6yXfoM6B+\n" +
    "XwIhAJZV1vaarQPNEeFsabMjTK0y0Vz4h3Tgl6PIF98am/E1AiBmlDFPqotX0Ero\n" +
    "nZHQS8FX1T6w7KzFaCcrO0HNdDn2uQIgMoR1DhI9ZGqR3qPTO0LEyUpLt6XuxCX8\n" +
    "DLOXoOLeUS8=\n" +
    "-----END PRIVATE KEY-----";
const publicKey = "-----BEGIN PUBLIC KEY-----\n" +
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAIVp+9oiYyNYOt3p1q0IkPPWcXGAmuOR\n" +
    "wSsS9iskOsmXzgoLCBYSURKQN1OvYTGJojwG2tQnPLHXatlnc//Sr+MCAwEAAQ==\n" +
    "-----END PUBLIC KEY-----";
const sign = new rsa(privateKey);
const verify = new rsa(publicKey);

const message = 'Nj0MH7b8nrZw1v0EpDuAvVenc5BOntxqQkXmaRwokR33ndI0Vbk8yGJsHNQIDHydzUQGLaV3VzI8przOi2yrUg==';
const decipher = sign.decrypt(message, 'utf8');
console.log(decipher);

test1 = "-----BEGIN PRIVATE KEY-----\n"+"MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlymBiVNEPpTopgT9\n"+"Cs0jCN7UAfn3VmCyI8wNmz0Xsveg1WnnrBTzWlNF0N+b9EibtXKeTFD+Ayfh5nHS\n"+"g5bHyQIDAQABAkBmRyAtgZiAW5Lami94enpFCzgZqj8vQ7fkvrFKI1kArr2rLYdW\n"+"nV5D14v5ogl2SYP00kbTDzx/2vm0zCjyArgBAiEA4IsTHrFkx4V6fbxLSwxj8bFq\n"+"Ynx8xl/h/ziMg6eulskCIQCsVripGVP/UyXO8Bk8tCARlyMcHXpU3eoH7duHnrIp\n"+"AQIhANMCfsZCKBXDnreYAh2VmDph4jqJB+yX4FYqOwnhwxTZAiEAjCArH1s3wAe0\n"+"WzE/4+q1lHfmFUsml3CkhHPzJq9zPwECIBGIDyL6CbMY8D0OSOpaCVl+tLfJ5q/q\n"+"AG9wMzohQOmL\n"+"-----END PRIVATE KEY-----"
test2 = "-----BEGIN PRIVATE KEY-----\n" +
    "MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlymBiVNEPpTopgT9\n" +
    "Cs0jCN7UAfn3VmCyI8wNmz0Xsveg1WnnrBTzWlNF0N+b9EibtXKeTFD+Ayfh5nHS\n" +
    "g5bHyQIDAQABAkBmRyAtgZiAW5Lami94enpFCzgZqj8vQ7fkvrFKI1kArr2rLYdW\n" +
    "nV5D14v5ogl2SYP00kbTDzx/2vm0zCjyArgBAiEA4IsTHrFkx4V6fbxLSwxj8bFq\n" +
    "Ynx8xl/h/ziMg6eulskCIQCsVripGVP/UyXO8Bk8tCARlyMcHXpU3eoH7duHnrIp\n" +
    "AQIhANMCfsZCKBXDnreYAh2VmDph4jqJB+yX4FYqOwnhwxTZAiEAjCArH1s3wAe0\n" +
    "WzE/4+q1lHfmFUsml3CkhHPzJq9zPwECIBGIDyL6CbMY8D0OSOpaCVl+tLfJ5q/q\n" +
    "AG9wMzohQOmL\n" +
    "-----END PRIVATE KEY-----";
console.log(test1 == test2)

t = '-----BEGIN PRIVATE KEY-----\nMIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlymBiVNEPpTopgT9\nCs0jCN7UAfn3VmCyI8wNmz0Xsveg1WnnrBTzWlNF0N+b9EibtXKeTFD+Ayfh5nHS\ng5bHyQIDAQABAkBmRyAtgZiAW5Lami94enpFCzgZqj8vQ7fkvrFKI1kArr2rLYdW\nnV5D14v5ogl2SYP00kbTDzx/2vm0zCjyArgBAiEA4IsTHrFkx4V6fbxLSwxj8bFq\nYnx8xl/h/ziMg6eulskCIQCsVripGVP/UyXO8Bk8tCARlyMcHXpU3eoH7duHnrIp\nAQIhANMCfsZCKBXDnreYAh2VmDph4jqJB+yX4FYqOwnhwxTZAiEAjCArH1s3wAe0\nWzE/4+q1lHfmFUsml3CkhHPzJq9zPwECIBGIDyL6CbMY8D0OSOpaCVl+tLfJ5q/q\nAG9wMzohQOmL\n-----END PRIVATE KEY-----'
console.log(test2 == t)
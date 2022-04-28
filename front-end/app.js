class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            micButton: document.querySelector('.mic__button'),
            addressButton: document.querySelector('.chat_opt_address'),
            phonenoButton: document.querySelector('.chat_opt_phoneno'),
        }
        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton, micButton, addressButton, phonenoButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        micButton.addEventListener('click', () => this.onSpeechtoText(chatBox))
        addressButton.addEventListener('click', () => this.addressChat(chatBox))
        phonenoButton.addEventListener('click', () => this.phoneChat(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    addressChat(chatbox){
        let address = { name: "BOT", message: "Vikas Nagar, Gyan Vikas Road, Sector 4, Kopar Khairane, Navi Mumbai, Maharashtra 400709" };
        this.messages.push(address);
        this.updateChatText(chatbox)
        textField.value = ''
    }

    phoneChat(chatbox){
        let phone = { name: "BOT", message: "022 2754 1005" };
        this.messages.push(phone);
        this.updateChatText(chatbox)
        textField.value = ''
    }



    toggleState(chatbox) {
        this.state = !this.state;
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSpeechtoText(chatbox) {
        var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
        var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList;
        var SpeechRecognitionEvent =
          SpeechRecognitionEvent || webkitSpeechRecognitionEvent;
           var grammar =""
  
        var recognition = new SpeechRecognition();
        var speechRecognitionList = new SpeechGrammarList();
        speechRecognitionList.addFromString(grammar, 1);
        recognition.grammars = speechRecognitionList;
        recognition.continuous = false;
        recognition.lang = "en-US";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
  
           recognition.start();

        recognition.onresult = function (event) {
        var textField = chatbox.querySelector('input');
  
          console.log(event.results[0][0].transcript);
          var color = event.results[0][0].transcript;
          textField.value += color;
          diagnostic.textContent = "Result received: " + color + ".";   
          bg.style.backgroundColor = color;
        };
  
        recognition.onspeechend = function () {
          recognition.stop();
        };
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

       fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json() )
          .then(r => {
            let msg2 = { name: "BOT", message: r.output };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          }).catch((error) => {console.log(error)});
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "BOT")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();
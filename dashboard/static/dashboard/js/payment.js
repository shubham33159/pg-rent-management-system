document.getElementById("pay-button").addEventListener("click", function() {

    fetch("/create-payment-order/")
        .then(response => response.json())
        .then(data => {

            const options = {
                key: razorpayKeyId,
                amount: data.amount * 100,
                currency: data.currency,
                order_id: data.order_id,

                handler: function(response) {

                    fetch("/verify-payment/", {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrfToken
                        },

                        body: JSON.stringify({
                            razorpay_order_id: response.razorpay_order_id,
                            razorpay_payment_id: response.razorpay_payment_id,
                            razorpay_signature: response.razorpay_signature
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                    });
                }
            };

            const razorpayCheckout = new Razorpay(options);

            razorpayCheckout.open();
        });
});
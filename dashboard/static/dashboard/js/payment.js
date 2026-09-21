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

            razorpayCheckout.on("payment.failed", function(response) {

                console.log("🔥 PAYMENT FAILED EVENT FIRED");
                console.log(response);
                console.log(response.error);

            });


            // razorpayCheckout.on("payment.failed", function(response){
            //     console.log("Payment failed", response.error);

            //     fetch("/payment-failed/",{
            //         method: "POST",
            //         headers: {
            //             "Content-Type": "application/json",
            //             "X-CSRFToken": csrfToken
            //         },
                    
            //         body: JSON.stringify({
            //             razorpay_order_id: response.error.metadata.order_id,
            //             razorpay_payment_id: response.error.metadata.payment_id,
            //             error_code: response.error.code,
            //             error_description: response.error.description

            //         })
            //     })
            //     .then(response => response.json())
            //     .then(data => {
            //         console.log(data)
            //     });
            // });

            razorpayCheckout.open();
        });
});
document.getElementById("pay-button").addEventListener("click", function() {
    console.log("Payment JS loaded");
    fetch("/create-payment-order/")
        .then(response => response.json())
        .then(data => {

            let paymentFailed = false;
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
                        console.log("Django response:", data);

                        if (data.status === "success") {
                            window.location.reload();
                        }
                    })
                    .catch(error => {
                        console.error("Verification error:", error);
                    });
                },
                modal: {
                    ondismiss: function() {

                        console.log("Razorpay popup closed");

                        if (paymentFailed) {
                            window.location.reload();
                        }
                    }
                }
            };

            const razorpayCheckout = new Razorpay(options);

            console.log("Razorpay object created");


            console.log("Failure listener registered");

            razorpayCheckout.on("payment.failed", function(response) {

                console.log("Payment failed:", response.error);

                paymentFailed = true;
                fetch("/payment-failed/", {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },

                    body: JSON.stringify({
                        razorpay_order_id: data.order_id,
                        error_code: response.error.code,
                        error_description: response.error.description
                    })
                })
                .then(response => {
                    console.log("HTTP status:", response.status);
                    return response.json();
                })
                .then(data => {
                    console.log("Django response:", data);
                })
                .catch(error => {
                    console.error("Fetch error:", error);
                });
            });

            razorpayCheckout.open();
        });
});
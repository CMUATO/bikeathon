"use strict";

function updateTime(start) {
  let elapsed = Date.now() - start;
  let seconds = Math.floor(elapsed / 1000);
  let minutes = Math.floor(seconds / 60);
  let hours = Math.floor(minutes / 60);

  minutes = "0" + String(minutes % 60);
  seconds = "0" + String(seconds % 60);

  let display = `${hours}:${minutes.slice(-2)}:${seconds.slice(-2)}`;
  $("#time").html(display);
}

function initTimer() {
  let start = Date.parse("13 Nov 2017 16:00:00 UTC");
  updateTime(start);
  let interval = setInterval(function () {
      updateTime(start);
  }, 1000);
}

function stripeTokenHandler(token) {
  var a = 1;
}

function stripeSetup() {
  var stripe = Stripe('pk_test_6pRNASCoBOKtIshFeQd4XMUh');

  // Create an instance of Elements
  var elements = stripe.elements();

  // Custom styling can be passed to options when creating an Element.
  // (Note that this demo uses a wider set of styles than the guide below.)
  var style = {
    base: {
      color: '#32325d',
      fontFamily: 'sans-serif',
      fontSmoothing: 'antialiased',
      fontSize: '16px',
      '::placeholder': {
        color: '#aab7c4'
      }
    },
    invalid: {
      color: '#fa755a',
      iconColor: '#fa755a'
    }
  };

  // Create an instance of the card Element
  var card = elements.create('card', {style: style});

  // Add an instance of the card Element into the `card-element` <div>
  card.mount('#card-element');

  // Handle real-time validation errors from the card Element.
  card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
      displayError.textContent = event.error.message;
    } else {
      displayError.textContent = '';
    }
  });

  // Handle form submission
  var form = document.getElementById('payment-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();

    stripe.createToken(card).then(function(result) {
      if (result.error) {
        // Inform the user if there was an error
        var errorElement = document.getElementById('card-errors');
        errorElement.textContent = result.error.message;
      } else {
        // Send the token to your server
        stripeTokenHandler(result.token);
      }
    });
  });
}

function initDonate() {
  $("#donate-button").click(function () {
    $("#payment-wrapper").fadeIn();
  });
  $("#cancel-button").click(function () {
    $("#payment-wrapper").fadeOut();
  })
}

function updateDistance() {
  let url = "http://flask-env.2rm2zjheap.us-east-1.elasticbeanstalk.com";
  $.get(url, function (text) {
    let data = JSON.parse(text);
    let distance = data["distance"];
    $("#distance").html(`${distance} miles`);
  });
}

function initDistance() {
  updateDistance();
  let interval = setInterval(function () {
    updateDistance();
  }, 10000);
}

window.addEventListener("DOMContentLoaded", function () {
  stripeSetup();
  initTimer();
  initDonate();
  initDistance();
});

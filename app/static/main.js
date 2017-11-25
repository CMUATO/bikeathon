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

function stripeTokenHandler(token, amount) {
  let params = {
    token: token,
    amount: amount
  };
  $.post("/charge-ajax", params, function (text) {
    let data = JSON.parse(text);
    if (data["success"] === 1) {
      $("#payment-wrapper").fadeOut();
      Materialize.toast('Thank you for your donation!', 10000);
    } else {
      $("#card-errors").text(data["message"]);
    }
  });
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
      displayError.innerHTML = '&nbsp;';
    }
  });

  // Handle form submission
  var form = document.getElementById('payment-form');
  form.addEventListener('submit', function(event) {
    event.preventDefault();

    $('#amount-errors').html('&nbsp;');

    var amount = $('#amount').val();
    amount = amount.replace(/\$/g, '').replace(/\,/g, '');

    amount = parseFloat(amount);

    if (isNaN(amount)) {
      $('#amount-errors').text('Please enter a valid amount');
    } else if (amount < 1.00) {
      $('#amount-errors').text('Donation amount must be at least $1');
    } else {
      amount = Math.round(amount * 100);
      stripe.createToken(card).then(function(result) {
        if (result.error) {
          // Inform the user if there was an error
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // Send the token to your server
          stripeTokenHandler(result.token.id, amount);
        }
      });
    }
  });
}

function processAmount() {
  let elem = $("#amount");
  let amount = parseFloat(elem.val());
  if (!isNaN(amount)) {
    elem.val(amount.toFixed(2));
  }
}

function initDonate() {
  $("#donate-button").click(function () {
    $("#payment-wrapper").fadeIn();
  });
  $("#cancel-button").click(function () {
    $("#payment-wrapper").fadeOut();
  });
  processAmount();
  $("#amount").change(processAmount);
}

function updateStats() {
  let url = "/stats";
  $.get(url, function (text) {
    let data = JSON.parse(text);
    let distance = data["distance"];
    let money = data["money"];
    $("#distance").text(`${distance} miles`);
    $("#money").text(`$${money}`)
  });
}

function initStats() {
  updateStats();
  let interval = setInterval(function () {
    updateStats();
  }, 10000);
}

window.addEventListener("DOMContentLoaded", function () {
  stripeSetup();
  initTimer();
  initDonate();
  initStats();
});

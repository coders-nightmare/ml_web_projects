// var canvas = document.getElementById("myCanvas");
// var context = canvas.getContext("2d");
// var mouse = { x: 0, y: 0 };
// canvas.addEventListener(
//   "mousedown",
//   function (e) {
//     console.log("mouse event triggered");
//     context.moveTo(mouse.x, mouse.y);
//     context.beginPath();
//     canvas.addEventListener("mousemove", onPaint, false);
//   },
//   false
// );
// var onPaint = function () {
//   context.lineTo(mouse.x, mouse.y);
//   context.stroke();
// };

// canvas.addEventListener(
//   "mouseup",
//   function () {
//     // $("#number").html('<img id="spinner" src="spinner.gif"/>');
//     canvas.removeEventListener("mousemove", onPaint, false);
//     var img = new Image();
//     img.onload = function () {
//       context.drawImage(img, 0, 0, 28, 28);
//       data = context.getImageData(0, 0, 28, 28).data;
//       var input = [];
//       for (var i = 0; i < data.length; i += 4) {
//         input.push(data[i + 2] / 255);
//       }
//       predict(input);
//     };
//     img.src = canvas.toDataURL("image/png");
//   },
//   false
// );

//gpt
var canvas = document.getElementById("canvas");
var context = canvas.getContext("2d");
var mouse = { x: 0, y: 0 };
var isDrawing = false;

// Set the desired canvas dimensions
var canvasSize = 280;
canvas.width = canvasSize;
canvas.height = canvasSize;

canvas.addEventListener("mousedown", function (e) {
  isDrawing = true;
  mouse.x = e.pageX - this.offsetLeft;
  mouse.y = e.pageY - this.offsetTop;
  context.moveTo(mouse.x, mouse.y);
});

canvas.addEventListener("mousemove", function (e) {
  if (isDrawing) {
    mouse.x = e.pageX - this.offsetLeft;
    mouse.y = e.pageY - this.offsetTop;
    draw();
  }
});

canvas.addEventListener("mouseup", function () {
  isDrawing = false;
  predictDigit();
});

canvas.addEventListener("mouseleave", function () {
  isDrawing = false;
});

function draw() {
  context.lineTo(mouse.x, mouse.y);
  context.stroke();
}

function clearCanvas() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  document.getElementById("number").innerText = "";
}

function preprocessCanvas() {
  // Resize and preprocess the canvas image
  var resizedCanvas = document.createElement("canvas");
  var resizedContext = resizedCanvas.getContext("2d");
  resizedCanvas.width = 28;
  resizedCanvas.height = 28;
  resizedContext.drawImage(canvas, 0, 0, 28, 28);

  var imgData = resizedContext.getImageData(0, 0, 28, 28);
  var input = [];
  var data = imgData.data;
  for (var i = 0; i < data.length; i += 4) {
    input.push(data[i + 2] / 255);
  }

  return input;
}

function predictDigit() {
  var input = preprocessCanvas();
  var tensor = tf.tensor(input).reshape([1, 28, 28, 1]);

  tf.loadLayersModel("model/model.json").then(function (model) {
    var prediction = model.predict(tensor);
    var predictedValue = tf.argMax(prediction.dataSync()).dataSync()[0];
    document.getElementById("number").innerText = predictedValue;
  });
}

document.getElementById("clear").addEventListener("click", clearCanvas);

// // Setting up tfjs with the model we downloaded
// tf.loadLayersModel("./model/model.json").then(function (model) {
//   window.model = model;
// });

// // Predict function
// var predict = function (input) {
//   if (window.model) {
//     window.model
//       .predict([tf.tensor(input).reshape([1, 28, 28, 1])])
//       .array()
//       .then(function (scores) {
//         scores = scores[0];
//         predicted = scores.indexOf(Math.max(...scores));
//         $("#number").html(predicted);
//       });
//   } else {
//     // The model takes a bit to load,
//     // if we are too fast, wait
//     setTimeout(function () {
//       predict(input);
//     }, 50);
//   }
// };

// Assuming 'randomImage' is the variable holding your random image data
// var img = new Image();
// img.onload = function () {
//   // Create a temporary canvas to resize the image
//   var tempCanvas = document.createElement("canvas");
//   var tempContext = tempCanvas.getContext("2d");

//   // Define the desired dimensions for the resized image
//   var resizedWidth = 28;
//   var resizedHeight = 28;

//   // Resize the image on the temporary canvas
//   tempCanvas.width = resizedWidth;
//   tempCanvas.height = resizedHeight;
//   tempContext.drawImage(img, 0, 0, resizedWidth, resizedHeight);

//   // Draw the resized image onto the main canvas
//   tempContext.drawImage(tempCanvas, 0, 0);

//   // Convert the image data into input format for the model
//   var imageData = tempContext.getImageData(
//     0,
//     0,
//     tempCanvas.width,
//     tempCanvas.height
//   ).data;
//   var input = [];
//   for (var i = 0; i < imageData.length; i += 4) {
//     input.push(imageData[i + 2] / 255);
//   }

//   // Call the predict function with the input data
//   predict(input);
// };

// // Set the src of the image to your random image URL or data
// img.src = "./images/imgSample.png";

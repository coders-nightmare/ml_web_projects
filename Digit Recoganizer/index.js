const express = require("express");
const app = express();
const path = require("path");

app.use(express.static("./public"));

app.set("views", path.join(__dirname, "/views"));

app.set("view engine", "ejs");
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.get("/", (req, res) => {
  res.render("main");
});

app.listen(5000, () => {
  console.log("the server is running on port 5000");
});

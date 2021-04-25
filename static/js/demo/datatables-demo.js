// Call the dataTables jQuery plugin

var accountData = $('#accountData').DataTable();
var courseData = $('#courseData').DataTable();
var labData = $('#labData').DataTable();

var accountDataCount = accountData.rows().count()
var courseDataCount = courseData.rows().count()
var labDataCount = labData.rows().count()

document.getElementById("accountDataCount").innerHTML = accountDataCount;
document.getElementById("courseDataCount").innerHTML = courseDataCount;
document.getElementById("labDataCount").innerHTML = labDataCount;


$(document).ready(function() {
  $accountData.DataTable();
});
$(document).ready(function() {
  $courseData.DataTable();
});
$(document).ready(function() {
  $labData.DataTable();
});
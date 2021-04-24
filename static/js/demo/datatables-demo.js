// Call the dataTables jQuery plugin

var accountData = $('#accountData').DataTable();
var courseData = $('#courseData').DataTable();
var sectionData = $('#sectionData').DataTable();

var accountDataCount = accountData.rows().count()
var courseDataCount = courseData.rows().count()
var sectionDataCount = sectionData.rows().count()

document.getElementById("accountDataCount").innerHTML = accountDataCount;
document.getElementById("courseDataCount").innerHTML = courseDataCount;
document.getElementById("sectionDataCount").innerHTML = sectionDataCount;


$(document).ready(function() {
  $accountData.DataTable();
});
$(document).ready(function() {
  $courseData.DataTable();
});
$(document).ready(function() {
  $sectionData.DataTable();
});
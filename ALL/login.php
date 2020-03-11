<?php
$connect = @mysql_connect("localhost","root","1234") or die("error");
$dbname = "android_test(user)";
$dbconn = mysql_select_db($dbname,$connect);
$username = $_POST['id'];

$query_search = "select * from custom_info where u_id = '".$username."' AND u_pw = '".$password. "'";
$password = $_POST['pw'];
$query_exec = mysql_query($query_search) or die(mysql_error());
echo "User Found";
$rows = mysql_num_rows($query_exec);

if($rows == 0) {
    echo "No Such User Found";
}
else  {
}
?>
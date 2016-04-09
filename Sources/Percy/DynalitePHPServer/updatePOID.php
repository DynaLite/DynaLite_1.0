<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$db->updatePOID($_POST['email'], $_POST['p_o_id']);

?>
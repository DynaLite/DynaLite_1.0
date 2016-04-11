<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$users = $db->getUsers();
 
if ($users != false) {
    // use is found
    $response["error"]=FALSE;
    $response["count"]=count($users);
    for($index=0; $index<count($users); $index++){
        $response[$index]["p_o_id"] = $users[$index]["p_o_id"];
    }
    
    echo json_encode($response);
} else {
    // user is not found with the credentials
    $response["error"] = TRUE;
    echo json_encode($response);
}
?>
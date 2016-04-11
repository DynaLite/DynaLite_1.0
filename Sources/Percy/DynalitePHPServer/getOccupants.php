<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$occupants = $db->getOccupants();
 
if ($occupants != false) {
    // use is found
    $response["error"]=FALSE;
    $response["count"]=count($occupants);
    for($index=0; $index<count($occupants); $index++){
        $response[$index]["p_o_id"] = $occupants[$index]["p_o_id"];
        $response[$index]["location"] = $occupants[$index]["location"];
    }
    
    echo json_encode($response);
} else {
    // user is not found with the credentials
    $response["error"] = TRUE;
    echo json_encode($response);
}
?>
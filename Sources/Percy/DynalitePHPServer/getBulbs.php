<?php
require_once 'DB_Functions.php';
$db = new DB_Functions();
 
// json response array
$response = array("error" => FALSE);
 
$bulbs = $db->getBulbs();
 
if ($bulbs != false) {
    // use is found
    $response["error"]=FALSE;
    $response["count"]=count($bulbs);
    for($index=0; $index<count($bulbs); $index++){
        $response[$index]["name"] = $bulbs[$index]["name"];
        $response[$index]["location"] = $bulbs[$index]["location"];
        $response[$index]["color"] = $bulbs[$index]["color"];
        $response[$index]["isON"] = $bulbs[$index]["isON"];
    }
    
    echo json_encode($response);
} else {
    // user is not found with the credentials
    $response["error"] = TRUE;
    echo json_encode($response);
}
?>
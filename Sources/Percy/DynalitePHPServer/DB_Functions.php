<?php

class DB_Functions {
 
    private $conn;
 
    // constructor
    function __construct() {
        require_once 'DB_Connect.php';
        // connecting to database
        $db = new Db_Connect();
        $this->conn = $db->connect();
    }
 
    // destructor
    function __destruct() {
         
    }
 
    /**
     * Storing new user
     * returns user details
     */
    public function storeUser($name, $email, $password) {
        $uuid = uniqid('', true);
        $hash = $this->hashSSHA($password);
        $encrypted_password = $hash["encrypted"]; // encrypted password
        $salt = $hash["salt"]; // salt
 
        $stmt = $this->conn->prepare("INSERT INTO users(unique_id, name, email, encrypted_password, salt, created_at) VALUES(?, ?, ?, ?, ?, NOW())");
        $stmt->bind_param("sssss", $uuid, $name, $email, $encrypted_password, $salt);
        $result = $stmt->execute();
        $stmt->close();
 
        // check for successful store
        if ($result) {
            $stmt = $this->conn->prepare("SELECT * FROM users WHERE email = ?");
            $stmt->bind_param("s", $email);
            $stmt->execute();
            $user = $stmt->get_result()->fetch_assoc();
            $stmt->close();
 
            return $user;
        } else {
            return false;
        }
    }

    public function getBulbs() {
 
        $stmt = $this->conn->prepare("SELECT * FROM bulbs");
 
        if ($stmt->execute()) {
            $result = $stmt->get_result();
            $lights = array();
            while($light = $result->fetch_assoc()){
                array_push($lights, $light);
            }
            $stmt->close();

            return $lights;
        } else {
            return NULL;
        }
    }

    public function getUsers() {
 
        $stmt = $this->conn->prepare("SELECT p_o_id FROM users");
 
        if ($stmt->execute()) {
            $result = $stmt->get_result();
            $users = array();
            while($user = $result->fetch_assoc()){
                array_push($users, $user);
            }
            $stmt->close();

            return $users;
        } else {
            return NULL;
        }
    }

    public function getOccupants() {
 
        $stmt = $this->conn->prepare("SELECT users.p_o_id as p_o_id, location.location as location FROM users INNER JOIN location ON users.id=location.user_id");
 
        if ($stmt->execute()) {
            $result = $stmt->get_result();
            $occupants = array();
            while($occupant = $result->fetch_assoc()){
                array_push($occupants, $occupant);
            }
            $stmt->close();

            return $occupants;
        } else {
            return NULL;
        }
    }

    public function updateColor($location, $color) {
        
        $stmt = $this->conn->prepare("UPDATE bulbs SET color=?, isON=1 WHERE location = ?");
 
        $stmt->bind_param("ss", $color, $location);
 
        $stmt->execute();
    }

    public function updateLocation($id, $location) {
        $stmt = $this->conn->prepare("SELECT * from location WHERE user_id = ?");
 
        $stmt->bind_param("s", $id);
 
        $stmt->execute();
 
        $stmt->store_result();
 
        if ($stmt->num_rows > 0) {
            // existed 
            $stmt->close();
            $isUserLocationExisted = true;
        } else {
            // not existed
            $stmt->close();
            $isUserLocationExisted = false;
        }

        if($isUserLocationExisted){
            $stmt = $this->conn->prepare("UPDATE location SET update_at=NOW(), location=? WHERE user_id = ?");
 
            $stmt->bind_param("ss", $location, $id);
 
            $stmt->execute();
        }
        else{
            $stmt = $this->conn->prepare("INSERT INTO location(user_id, location) VALUES(?, ?)");
 
            $stmt->bind_param("ss", $id, $location);
 
            $stmt->execute();
        }

        return true;
    }

    public function updatePOID($email, $p_o_id) {
        
        $stmt = $this->conn->prepare("UPDATE users SET update_at=NOW(), p_o_id=? WHERE email = ?");
 
        $stmt->bind_param("ss", $p_o_id, $email);
 
        $stmt->execute();

        return true;
    }
 
    /**
     * Get user by email and password
     */
    public function getUserByEmailAndPassword($email, $password) {
 
        $stmt = $this->conn->prepare("SELECT * FROM users WHERE email = ?");
 
        $stmt->bind_param("s", $email);
 
        if ($stmt->execute()) {
            $user = $stmt->get_result()->fetch_assoc();
            $stmt->close();
 
            // verifying user password
            $salt = $user['salt'];
            $encrypted_password = $user['encrypted_password'];
            $hash = $this->checkhashSSHA($salt, $password);
            // check for password equality
            if ($encrypted_password == $hash) {
                // user authentication details are correct
                return $user;
            }
        } else {
            return NULL;
        }
    }
 
    /**
     * Check user is existed or not
     */
    public function isUserExisted($email) {
        $stmt = $this->conn->prepare("SELECT email from users WHERE email = ?");
 
        $stmt->bind_param("s", $email);
 
        $stmt->execute();
 
        $stmt->store_result();
 
        if ($stmt->num_rows > 0) {
            // user existed 
            $stmt->close();
            return true;
        } else {
            // user not existed
            $stmt->close();
            return false;
        }
    }
 
    /**
     * Encrypting password
     * @param password
     * returns salt and encrypted password
     */
    public function hashSSHA($password) {
 
        $salt = sha1(rand());
        $salt = substr($salt, 0, 10);
        $encrypted = base64_encode(sha1($password . $salt, true) . $salt);
        $hash = array("salt" => $salt, "encrypted" => $encrypted);
        return $hash;
    }
 
    /**
     * Decrypting password
     * @param salt, password
     * returns hash string
     */
    public function checkhashSSHA($salt, $password) {
 
        $hash = base64_encode(sha1($password . $salt, true) . $salt);
 
        return $hash;
    }
 
}
 
?>
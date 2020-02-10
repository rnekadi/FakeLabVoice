<?php 

$command = escapeshellcmd('/usr/custom/inference.py');
$output = shell_exec($command);
echo $output;

?>
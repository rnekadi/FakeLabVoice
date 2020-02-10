<html>
<head>
    </head>
<body>
    <a href="runPy.php">Predict</a>
    
    <?php 

$command = escapeshellcmd('/usr/custom/inference.py');
$output = shell_exec($command);
echo $output;

?>
    
    </body>
</html>
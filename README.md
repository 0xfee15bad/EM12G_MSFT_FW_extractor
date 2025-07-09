# Extracting the EM12-G MSFT firmware upgrade

The EM12-G MSFT was shipped with several Microsoft Surface devices, and they can now be found
for much cheaper than the regular EM12-G.

The downside is the customized firmware they run, which can't be upgraded to the "regular" one,
and can only be upgraded from a Surface device through Windows Updates (or manually).

These manual updates can be found in the big "Drivers and Firmware" package that Microsoft provides
for each Surface device :
* https://www.microsoft.com/en-us/download/details.aspx?id=102633
* https://www.microsoft.com/en-us/download/details.aspx?id=103503

And the latest firmware upgrade it has received dates back from March 2024 : `EM12GPAR01A16M4G_MSFT`

## Extract the MSI package

There are multiple options :

* The "official" way (Windows-only) : https://superuser.com/a/307679
* The portable way : https://pypi.org/project/python-msi/

## Locate the firmware upgrade package

In the subdirectory `quectelfwupdatedriver` you will find a file named `firmare.img`, which does not
seem to be usable outside of a Surface device either.

## Extract the firmware upgrade from it

* Clone this repository
* Install the (only) Python dependency from requirements.txt
* Run the script something like this :
```bash
./extract.py /path/to/extracted_msi/quectelfwupdatedriver/firmware.img
```

This will have created an `update` subdirectory with all the required files to upgrade the firmware of
your EM12-G MSFT module with the regular Quectel tools (QFlash / QFirehose) :

```bash
update
├── appsboot.mbn
├── firehose
│   ├── partition_complete_p4K_b256K.mbn
│   ├── patch_p4K_b256K.xml
│   ├── prog_firehose_9x65.mbn
│   └── rawprogram_nand_p4K_b256K_update.xml
├── NON-HLOS.ubi
├── rpm.mbn
├── sbl1.mbn
├── sdx20-boot.img
├── sdx20-cache.ubi
├── sdx20-recovery.ubi
├── sdx20-rootfs.ubi
├── sdx20-usrfs.ubi
└── tz.mbn
```

## Notes

This has been tested to upgrade a module from `EM12GPAR01A14M4G_MSFT` to `EM12GPAR01A16M4G_MSFT`, this
*should* work (or at least be pretty easy to adapt) if Microsoft ever releases a newer version.

### Before

```bash
$> echo ATI | sudo socat - /dev/ttyUSB3,crnl
ATI
Quectel
EM12
Revision: EM12GPAR01A14M4G_MSFT

OK
```

### After

```bash
$> echo ATI | sudo socat - /dev/ttyUSB3,crnl
ATI
Quectel
EM12
Revision: EM12GPAR01A16M4G_MSFT

OK
```

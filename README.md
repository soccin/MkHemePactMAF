# MkHemePactMAF: Generate MAF with match normal info

MkHemePactMAF generates a MAF where

* total depth
* reference depth
* alt allele depth
* alt allele frequency

for the matched normal sample is added for samples were the tumor was called against the pooled normal. This occurs often in HemePACT samples due to contamination of the normal samples. 

## Usage:

usage: ./MkHemePactMAF/mkHemePactMAF.sh DMP_ROOT_DIR

Example:

```bash
./MkHemePactMAF/mkHemePactMAF.sh /ifs/res/seq/younesa/asgariz/Proj_5270_F/r_001
```

Will generate the file:

* Proj_5270_F___HemeMAF.txt


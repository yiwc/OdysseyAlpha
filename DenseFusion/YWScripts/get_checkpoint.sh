cd ~
#https://drive.google.com/file/d/1gfOnOojzVdEwPzSaPmS3t3aJaQptbys6/view?usp=sharing
export fileid=1gfOnOojzVdEwPzSaPmS3t3aJaQptbys6
export filename=trained_checkpoints.zip

## WGET ##
wget --save-cookies cookies.txt 'https://docs.google.com/uc?export=download&id='$fileid -O- \
     | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1/p' > confirm.txt

wget --load-cookies cookies.txt -O $filename \
     'https://docs.google.com/uc?export=download&id='$fileid'&confirm='$(<confirm.txt)

## CURL ##
curl -L -c cookies.txt 'https://docs.google.com/uc?export=download&id='$fileid \
     | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1/p' > confirm.txt

curl -L -b cookies.txt -o $filename \
     'https://docs.google.com/uc?export=download&id='$fileid'&confirm='$(<confirm.txt)

rm -f confirm.txt cookies.txt
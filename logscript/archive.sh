#!/bin/bash
rm output/*
mv out_pdf/* output/out_pdf
mv out_csv/* output/out_csv
mv *pdf output
mv *csv output
tar -cvzf output.tar.gz output
rm output/out_csv/*
rmdir output/out_csv
rm output/*.csv
zip -r output_pdf.zip output
rm output/out_pdf/*
rmdir output/*
rm output/.DS_Store
rm output/*
rmdir output





IAS Project 

A steganographic technique by using both LSB substitution and PVD with in a block. The image is partitioned into 2×2 pixel blocks in a non-overlapping fashion. For every 2×2 pixel block the upper-left pixel is embedded with k-bits of data using LSB substitution. Then the new value of this pixel is used to calculate three pixel value differences with the upper-right, bottom-left, and bottom-right pixels of the block. Then data bits are hidden using these three difference
values in three directions. Both horizontal and vertical edges are considered.
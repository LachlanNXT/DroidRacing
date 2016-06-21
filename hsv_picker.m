close all;
startup_rvc;

im = iread('test_image_5.jpg', 'uint8');
im = rgb2hsv(im);
im = iint(im);
idisp(im);
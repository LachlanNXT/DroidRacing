test = iread('test_image_1.jpg', 'double');
%idisp(test);
R = test(:,:,1);
G = test(:,:,2);
B = test(:,:,3);
Y = R + G + B;
r = R./Y; g = G./Y; b = B./Y;
newim = test;
newim(:,:,1) = r;
newim(:,:,2) = g;
newim(:,:,3) = b;
%figure
idisp(newim);

blue = (r > 0) & (r < 0.25) & (b > 0.45) & (b < 1);
idisp(blue);

yellow = (r > 0.35) & (r < 0.45) & (b > 0) & (b < 0.3);
idisp(yellow);
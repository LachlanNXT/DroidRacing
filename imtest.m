test = {{},{},{},{},{},{},{},{},{},{},{}};
blue = {{},{},{},{},{},{},{},{},{},{},{}};
yellow = {{},{},{},{},{},{},{},{},{},{},{}};
newim = {{},{},{},{},{},{},{},{},{},{},{}};
for i = 1:11;

test{i} = iread(strcat('test_image_', num2str(i), '.jpg'), 'double');
%idisp(test);
R = test{i}(:,:,1);
G = test{i}(:,:,2);
B = test{i}(:,:,3);
Y = R + G + B;
r = R./Y; g = G./Y; b = B./Y;
newim{i} = test{i};
newim{i}(:,:,1) = r;
newim{i}(:,:,2) = g;
newim{i}(:,:,3) = b;
%figure
%idisp(newim);

blue{i} = (r > 0) & (r < 0.25) & (b > 0.4) & (b < 1);
%idisp(blue);

yellow{i} = (r > 0.35) & (r < 0.45) & (b > 0) & (b < 0.3);
%idisp(yellow);

end
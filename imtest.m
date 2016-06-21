close all;
startup_rvc;

im = {{},{},{},{},{},{},{},{},{},{},{}};
blue = {{},{},{},{},{},{},{},{},{},{},{}};
yellow = {{},{},{},{},{},{},{},{},{},{},{}};
chroma = {{},{},{},{},{},{},{},{},{},{},{}};

for i = 1:21;
    im{i} = iread(strcat('test_image_', num2str(i), '.jpg'), 'double');
    %idisp(test);
    R = im{i}(:,:,1);
    G = im{i}(:,:,2);
    B = im{i}(:,:,3);
    Y = R + G + B;
    r = R./Y;
    g = G./Y;
    b = B./Y;
    
    chroma{i} = im{i};
    chroma{i}(:,:,1) = r;
    chroma{i}(:,:,2) = g;
    chroma{i}(:,:,3) = b;

    blue{i} = (r > 0.12) & (r < 0.16) & (g > 0.3) & (g < 0.34) & (b > 0.38) & (b < 0.6);
    yellow{i} = (r > 0.38) & (r < 0.43) & (g > 0.34) & (g < 0.4) & (b > 0.18) & (b < 0.27);
    
    %figure(i);  
    %idisp([blue{i} yellow{i}]);
end
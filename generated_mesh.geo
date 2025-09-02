// Rectangle with circular hole - refined mesh example

// Geometry parameters
rect_width = 10;
rect_height = 5;
hole_radius = 1;

// Rectangle points
Point(1) = {-rect_width/2, -rect_height/2, 0};
Point(2) = {rect_width/2, -rect_height/2, 0};
Point(3) = {rect_width/2, rect_height/2, 0};
Point(4) = {-rect_width/2, rect_height/2, 0};

// Rectangle edges
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

// Circle definition
Point(5) = {0, 0, 0}; // Center
Point(6) = {hole_radius, 0, 0};
Point(7) = {0, hole_radius, 0};
Point(8) = {-hole_radius, 0, 0};
Point(9) = {0, -hole_radius, 0};

// Circle arcs
Circle(5) = {6, 5, 7};
Circle(6) = {7, 5, 8};
Circle(7) = {8, 5, 9};
Circle(8) = {9, 5, 6};

// Line loops and surfaces
Line Loop(1) = {1, 2, 3, 4}; // Outer rectangle
Line Loop(2) = {5, 6, 7, 8}; // Inner circle
Plane Surface(1) = {1, 2}; // Surface with hole

// Mesh size parameters
base_size = 1.0; // Coarse size away from hole
fine_size = 0.1; // Fine size near hole

// Size field for refinement
Field[1] = Distance;
Field[1].NodesList = {5}; // Center point
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = fine_size;
Field[2].LcMax = base_size;
Field[2].DistMin = hole_radius;
Field[2].DistMax = 2*hole_radius;

// Use the threshold field
Background Field = 2;

// Physical groups
Physical Curve("OuterBoundary") = {1, 2, 3, 4};
Physical Curve("InnerCircle") = {5, 6, 7, 8};
Physical Surface("Domain") = {1};

// Mesh settings
Mesh.Algorithm = 6; // Frontal-Delaunay
Mesh.Smoothing = 5;

// Generate 2D mesh
Mesh 2;
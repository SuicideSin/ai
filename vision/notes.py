'''
Assignments:


Edge detection:
    Color differential
    Pixel values differnt
    
    a.k.a. Intensity difference peaks
    
    gradient, Gx = (-1 0 1)
                   (-2 0 2)
                   (-1 0 1)
                   
              Gy = ( 1  2  1)
                   ( 0  0  0)
                   (-1 -2 -1)
                     
            this is the derivative in the x or y direction
    
            Gx^2 + Gy^2 > T
            
            
Improving Sobel:
    thin the edges,
    refine the edges
        remove noise, connect certain edges


    Canny Edge detection:
        Consider potential edge pixel p to nearest neighbors along the perpendicular to the supposed edge
        Only keep p as an edge if its G value is the maximum
        
    ø = atan2(Gy, Gx)

    Get rid of isolated artifacts:
        

Hough transforms
How to identify circles:

started with an image, lot of pixels, information, make it grayscale, blur to reduce noise, sobel to detect edges, starting from a huge amount of information to represent the inherent message in the image
needs to understand the people in the image, but not necessarily the facial features
need to look for more features, not just edges
circles, maybe lines
sometimes in an image theres mostly a circle, but computer needs to understand that there is a circle, fill in edges for it
when you look at a picture you dont think wow how many circles are there

*random break*
in concrete, looking at tower of hanoi
we know how to solve with recursion
how do you solve it iteratively????
why should we bother... but if someone gave us the tower in an incomplete state, now your computer is screwed
when we solve the tower of hanoi, we can look at patterns
*back to lecture*

we would like to identify circles
given an image
we have found edge pixels
one possible way- three values to describe a circle (x, y, radius)
if I have three points on a circle, where is the center? use velkoz mechanics
in an image of n endpoints, how many times do I have to look through to find center of all triples of edge values
once i have all those centers figured out, which point has the most centers
suppose n edge pixels, how many distinct triples of edge pixels are there?
ans: n choose 3
(n*(n-1)*(n-2))/3! OR n!/[(n-3)!(3!)]
alternate way because first method has shitton of possibilites

more information in the edges than just points
we also have the GRADIENT, the direction that the edge is headed in
center is the perpendicular bisector of that direction
for every single edge pixel
take a blank canvas
take the gradient, the original gradient not the 4 directions
that gradient defines a line
so take that line and draw it on the canvas
and keep doing for every edge pixel
we find that a bunch of lines intersect at a single point.. do this for thursday

what does it mean to draw a line? if you keep drawing, how do you know that that pixel is a point of intersection? dont necessarily give it 255, give it increments of 1
they are not pixel values, they are simply numbers (# can be > 255)
at the end of drawing all the lines, rescale everything
who is the pixel that had the most passing through?
take that num (lets say 800) and divide by 255, scale it so that the point is the whitest
circles tend to be imperfect, so that the lines dont necessarily intersect at exactly the same point
usually groups of higher values, need to find the sections of higher values
could pass a window/filter over the neighbors and adds up all the array values
whoever is above a certain threshold, this is probably a center
whenever you run a program from now on, print height, width, number of edge pixels
might be more than one center, multiple circles going around. test with either a single circle or a rectangle, triangle, circle
they call this method boating... so is the computer motor boating ;o
monday- we have the centers, now find the radii
do this by
for every given center, ask what edge pixels contributed to this
each edge gets a vote in what the radius is
will end up with a graph that looks like a bell curve

Next Assignment (3/7/16):
    Identify lines:
        slope  = m = delta y/ delta x = tan(ø), where ø = angle the line makes with the x-axis
        
        |
        \ 
        |\ 
        | \ 
        |  \ 
        |   \ 
        |   /\.(p, q) 
        |  /  \ 
        | /d   \ 
        |/      \ ø
        /--------\--------------------
        
        ***Find d in terms of ø and (p,q), where d is the closest distance from the line to the origin
        
        e.g. (p,q) = (5,0)
             ø | d
             __|__
             0 | 0
             90| 5
             __|__ (5,5)
             0 | 5
             90| 5
             45| 0
            135| 5sqrt(2)
             __|__

        direction vector for line with angle ø:
        <cosø, sinø>


Good runs:
./circles.py https://s-media-cache-ak0.pinimg.com/236x/0c/0d/77/0c0d770cb43479255dbc1ee8b4d0c53a.jpg 8000 10000 140 1.6

./circles.py http://a.rgbimg.com/cache1n8lHa/users/j/ja/jazza/300/2djsZxD.jpg 8000 10000 60

./circles.py https://cdn.shopify.com/s/files/1/0080/8372/products/tattly_yoko_sakao_ohama_circle_web_design_01_grande.jpg?v=1444759102 8000 1000 100

./circles.py http://www.clipartbest.com/cliparts/7Ta/x9E/7Tax9ERTA.png 8000 10000 100

./circles.py http://archeryguide.net/wp-content/uploads/2012/04/archery-target.s600x6001.jpg 8000 10000 100

./circles.py http://cdn2.business2community.com/wp-content/uploads/2014/06/archery-target.jpg 8000 10000 70 1.2







'''
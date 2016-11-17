import sys
import pygame
import copy

SCREEN_SIZE   = 640,480

# Object dimensions
BRICK_WIDTH   = 60
BRICK_HEIGHT  = 15
PADDLE_WIDTH  = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
RED   = (255,0,0)
BRICK_COLOR = (0,255,255)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

class Bricka:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("BreakoutPredictor")
        
        self.clock = pygame.time.Clock()

        #self.font = pygame.font.Font(None,30)
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()
    
    '''
    The idea behind the solution is creating a copy of the ball called the predictor
    1. It is the same pygame.Rect object as the ball
    2. We also create a copy of the bricks
    3. So, the predictor is a ball with it's own set of bricks
    4. When the ball collides with (or, starts from the paddle) the predictor ball starts
       with the same initial conditions: same velocity and direction and same position
       It travels faster than the ball
    5. This is done by calling the move_predictor function 300 times per frame jump while
       the move_ball function is called just once per frame
    6. So, the predictor just moves exactly like the ball does but does it much before

    When the velocity increases over time:
    a. It was observed that the handle_collisions function behaves a bit differently
       when the ball moves with higher velocity. The ball actually digs a bit deeper into the 
       brick when the frame change happens. And since the COLLIDERECT pygame function checks 
       after every frame change, the ball actually might lead to a diffent path than the one it
       originally starts with.
    b. Therefore, the predictor is initialized to the same velocity and direction after every frame
    c. Thus, it just follows the ball and predicts the end position every frame.
       
    '''
        
    def init_game(self):
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE

        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        #Predictor Ball - Does the same thing as a regular ball except some things
        self.predictor_state = STATE_BALL_IN_PADDLE
        self.predictor     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)

        self.ball_vel = [5,-5]
        self.predictor_vel = [self.ball_vel[0],self.ball_vel[1]]

        self.create_bricks()
        
    #This function creates bricks on initialization
    #It also creates a copy of the bricks used for the predictor
    def create_bricks(self):
        y_ofs = 35
        self.bricks = []
        for i in range(7):
            x_ofs = 35
            for j in range(8):
                self.bricks.append(pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 5
        self.predictor_bricks = copy.deepcopy(self.bricks)

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    #def draw_predictor_bricks(self):
        #for predictor_brick in self.predictor_bricks:
            #pygame.draw.rect(self.screen, (200,200,0), predictor_brick)
        
    def check_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 6
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 6
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE:
            self.ball_vel = [5,-5]
            self.predictor_vel = [self.ball_vel[0],self.ball_vel[1]]
            self.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

        '''
        Fuzzy Controlled Paddle:
        '''

    def move_paddle(self):

        '''
        The distance from the ball to the paddle is divided into 4 brackets
        with each overlaping some other bracket. 
        The maximum distance that the ball can have from the paddle is 580 units
        as the game window itself is 640 units and the paddle width is 60 units.
        The 4 brackets and the corresponding rules are:
        1. [0,180] -> Velocity(paddle)=5 units/framecall
        2. [150,330] -> Velocity(paddle)=10 units/framecall
        3. [300,480] -> Velocity(paddle)=12.5 units/framecall
        4. [450,580] -> Velocity(paddle)=15 units/framecall

        The overlapping regions of:
        (150,180)
        (300,330)
        (450,480)
        are the regions where 2 rules fire.
        The velocity function, which contains 4 brackets itself, is then used to calculate the 
        center of mass of the area formed by the partial score of both rule functions.
        '''

        if self.predictor_vel==[0,0]:
            if 0<=self.paddle.left-self.predictor.left<=150:
                self.paddle.left -= 5
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 180<=self.paddle.left-self.predictor.left<=300:
                self.paddle.left -= 10
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 330<=self.paddle.left-self.predictor.left<=450:
                self.paddle.left -= 12.5
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 480<=self.paddle.left-self.predictor.left<=580:
                self.paddle.left -= 15.0
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 150<self.paddle.left-self.predictor.left<180:
                distance=self.paddle.left-self.predictor.left
                self.paddle.left -= float((float(distance)/30)*10+(1-(float(distance)/30))*5)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 300<self.paddle.left-self.predictor.left<330:
                distance=self.paddle.left-self.predictor.left
                self.paddle.left -= float((float(distance)/30)*12.5+(1-(float(distance)/30))*10)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left < 0:
                    self.paddle.left = 0
            if 580<self.paddle.left-self.predictor.left<450:
                distance=self.paddle.left-self.predictor.left
                self.paddle.left -= float((float(distance)/30)*15+(1-(float(distance)/30))*12.5)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left < 0:
                    self.paddle.left = 0
                
    #//This is the second function
            if 430<=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH):
                self.paddle.left += 15
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 280<=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<=400:
                self.paddle.left += 12.5
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 130<=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<=250:
                self.paddle.left += 10
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 0<=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<=130:
                self.paddle.left += 5
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 100<(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<130:
                distance=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)
                self.paddle.left += float((float(distance)/30)*10+(1-(float(distance)/30))*5)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 250<(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<280:
                distance=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)
                self.paddle.left += float((float(distance)/30)*12.5+(1-(float(distance)/30))*10)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X
            if 400<(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)<430:
                distance=(self.predictor.left+BALL_DIAMETER)-(self.paddle.left+PADDLE_WIDTH)
                self.paddle.left += float((float(distance)/30)*15+(1-(float(distance)/30))*12.5)/((float(distance)/30)+(1-(float(distance)/30)))
                if self.paddle.left > MAX_PADDLE_X:
                    self.paddle.left = MAX_PADDLE_X



    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:            
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    #Rules for moving the predictor are same as the ball
    def move_predictor(self):
        self.predictor.left += self.predictor_vel[0]
        self.predictor.top  += self.predictor_vel[1]

        if self.predictor.left <= 0:
            self.predictor.left = 0
            self.predictor_vel[0] = -self.predictor_vel[0]
        elif self.predictor.left >= MAX_BALL_X:
            self.predictor.left = MAX_BALL_X
            self.predictor_vel[0] = -self.predictor_vel[0]
        
        if self.predictor.top < 0:
            self.predictor.top = 0
            self.predictor_vel[1] = -self.predictor_vel[1]
        elif self.predictor.top >= MAX_BALL_Y:            
            self.predictor.top = MAX_BALL_Y
            self.predictor_vel[1] = -self.predictor_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
            ###
            ###
            #Changed only the predictor's state after the ball collides with the paddle
            self.predictor.top = PADDLE_Y - BALL_DIAMETER
            self.predictor.left = self.ball.left
            self.predictor_vel[1] = self.ball_vel[1]
            self.predictor_vel[0] = self.ball_vel[0]
            ###
            ###
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER

    #This function handles collisions of the predictor with the bricks
    #It's similar to the function that handles collisions for the ball
    def handle_predictor_collisions(self):
        for predictor_brick in self.predictor_bricks:
            if self.predictor.colliderect(predictor_brick):
                self.predictor_vel[1] = -self.predictor_vel[1]
                self.predictor_bricks.remove(predictor_brick)
                break

        if self.predictor.top > self.paddle.top:
            self.predictor_vel = [0,0]


    def show_stats(self):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
            self.screen.blit(font_surface, (205,5))

    def show_message(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))

            
    def run(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit

            self.clock.tick(50)
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:

                #Increase velocity over frames.
                #The velocity could be increased over "absolute" time and not over frames
                self.ball_vel[0]*=1.001
                self.ball_vel[1]*=1.001
                self.move_ball()
                self.handle_collisions()
                
                #-------- NOT NECESSARY IF CONST VEL ----------
                #Predictor starts from the ball state and then predicts it's movements further
                self.predictor.left=self.ball.left
                self.predictor.top=self.ball.top
                self.predictor_vel[0]=self.ball_vel[0]
                self.predictor_vel[1]=self.ball_vel[1]

                #----------------------------------------------

                for i in range(200):
                    self.move_predictor()
                    self.handle_predictor_collisions()
                self.move_paddle()

            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL")

                #predictor also moving with the paddle
                self.predictor.left = self.paddle.left + self.paddle.width / 2
                self.predictor.top  = self.paddle.top - self.predictor.height
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")
                
            self.draw_bricks()
            #self.draw_predictor_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS), BALL_RADIUS)

            # Draw predictor
            #if self.predictor_vel==[0,0]:
            pygame.draw.circle(self.screen, RED, (self.predictor.left + BALL_RADIUS, self.predictor.top + BALL_RADIUS), BALL_RADIUS)


            self.show_stats()
            pygame.display.flip()


if __name__ == "__main__":
    Bricka().run()

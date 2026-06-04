import pygame
import random
import math



pygame.init()
pygame.mixer.init()

song = r"C:\\Users\black\Audio Visual Detection Project\\audio\\test_songs\SpotiMate.io - Operator - Extended Mix - Arcando.mp3"

from audio.analyzer import analyze_audio

from ml.mood_classifier import train_model, predict_mood

training_songs = [

    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Kanine & Arcando - Lost Tonight (ft. HEIGHTS) - Arcando.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Hide U (Tinlicker Extended Remix).mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Calvin Harris - I'm Not Alone (MPH Remix - Official Audio) - CalvinHarrisVEVO.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Porter Robinson - Sad Machine (Official Lyric Video) - PorterRobinsonVEVO.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\ROSÉ x Bruno Mars - APT. (Dabin Remix).mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Seedhe Maut - Raat Ki Raani  (Lyrics) - Musicgenree.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Paresh Pahuja - Dooron Dooron (Live from The Voice Notes Concert) - Paresh Pahuja.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Kubbi _ Formed by Glaciers - Kubbi.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Chopin - Nocturne in E Flat Major (Op. 9 No. 2) - Rousseau.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Attack On Titan OST - Call of Silence (Ymir's Theme) - PianoDeuss.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\C418 - Aria Math (Minecraft Volume Beta) - NycrypticProject.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Fly Me To The Moon - Charles Cornell.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Für Elise - Reimagined - Alexander Joseph.mp3",
    r"C:\\Users\black\Audio Visual Detection Project\\audio\\train_songs\\Kygo & Selena Gomez - It Ain't Me (Audio) - KygoOfficialVEVO.mp3",
    

    ]
model = train_model(training_songs)
print(model.cluster_centers_)



data=analyze_audio(song)
print("Tempo:", data["tempo"])
mood = predict_mood(model, data)


print("Detected Mood:", mood)

if mood == "Energetic":
    particle_count = 100
    trail_alpha = 35
    palette = [
    (255,100,255),
    (220,80,255),
    (255,150,220),
    (180,80,255)
    ]

elif mood == "Calm":
    particle_count = 60
    trail_alpha = 20
    palette = [
    (120,180,255),
    (80,220,255),
    (180,220,255),
    (150,255,255)
    ]
    
elif mood == "Balanced":
    particle_count = 80
    trail_alpha = 30
    palette = [
    (140, 120, 255), 
    (120, 180, 255),
    (180, 140, 255), 
    (100, 220, 255)   
    ]

Width, Height = 1000, 500
pygame.display.set_caption("Audio Reactive Visual Engine")

pygame.mixer.music.load(song)
pygame.mixer.music.play()  
screen = pygame.display.set_mode((Width, Height))

                
clock = pygame.time.Clock()
time = 0

smooth_bass = 0
smooth_mid = 0
smooth_treble = 0

class Particle:
    def __init__(self):
        self.x = random.randint(0, Width)
        self.y = random.randint(0, Height)
        
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

        self.size = random.randint(3,4)


        self.color = random.choice(palette)

    def move(self,energy,time):
        self.x += self.vx * (1 + energy * 8)
        self.y += self.vy * (1 + energy * 8)

        if self.x <= 0 or self.x >= Width:
            self.vx *= -1

        if self.y <= 0 or self.y >= Height:
            self.vy *= -1
            
        self.vx *= 0.995
        self.vy *= 0.995   
        
    
        self.vx += math.sin(self.y * 0.01 + time) * 0.05
        self.vy += math.cos(self.x * 0.01 + time) * 0.05
        
        self.vx += random.uniform(-0.01, 0.01)
        self.vy += random.uniform(-0.01, 0.01)
            

    def draw(self, pulse):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.size + pulse)
        )
    def lines(brightness):
        
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):

                p1 = particles[i]
                p2 = particles[j]

                distance = math.sqrt(
                    (p1.x - p2.x) ** 2 +
                    (p1.y - p2.y) ** 2
                )

                if distance < 80:

                    pygame.draw.line(
                    screen,
                    (50, line_intensity, 255),
                    (int(p1.x), int(p1.y)),
                    (int(p2.x), int(p2.y)),
                    1
                    )
        
        
particles = [Particle() for _ in range(particle_count)]

pulse = 0

fade_surface = pygame.Surface((Width, Height))
fade_surface.set_alpha(trail_alpha)
fade_surface.fill((0, 0, 8))


#rms stuff
def get_current_rms(current_time):

    closest_index = min(
        range(len(data["rms_times"])),
        key=lambda i: abs(data["rms_times"][i] - current_time)
    )

    return data["rms"][closest_index]

def get_current_bass(current_time):

    closest_index = min(
        range(len(data["freq_times"])),
        key=lambda i: abs(data["freq_times"][i] - current_time)
    )

    return data["bass"][closest_index]

def get_current_mid(current_time):

    closest_index = min(
        range(len(data["freq_times"])),
        key=lambda i: abs(data["freq_times"][i] - current_time)
    )

    return data["mid"][closest_index]

def get_current_treble(current_time):

    closest_index = min(
        range(len(data["freq_times"])),
        key=lambda i: abs(data["freq_times"][i] - current_time)
    )

    return data["treble"][closest_index]

    
running = True
while running:
    clock.tick(60)
    current_time = pygame.mixer.music.get_pos() / 1000
    #rms stuff
    current_rms = get_current_rms(current_time)
    
    #fft analysis stuff 
    current_bass = get_current_bass(current_time)
    current_mid = get_current_mid(current_time)
    current_treble = get_current_treble(current_time) 
    
    smooth_bass = smooth_bass * 0.9 + current_bass * 0.1
    smooth_mid = smooth_mid * 0.9 + current_mid * 0.1
    smooth_treble = smooth_treble * 0.9 + current_treble * 0.1
    
    line_intensity = max(
    100, min(255, int(smooth_treble * 40+100)))
    
    bass_force = math.sqrt(smooth_bass) * 0.1
    flow_strength = smooth_mid * 0.002 
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.blit(fade_surface, (0, 0))

    pulse *= 0.9
    
    for beat in data["beat_times"]:
        if abs(current_time - beat) < 0.1:
            pulse = 8
            for particle in particles:
                particle.vx += random.uniform(-bass_force, bass_force)
                particle.vy += random.uniform(-bass_force, bass_force)
            
    Particle.lines(line_intensity)

    for particle in particles:
        particle.move(current_rms,time)
        particle.draw(pulse + current_rms * 8)

    pygame.display.flip()

    time += 0.03
    

    
    
    
    
    
  
    


pygame.quit()
    


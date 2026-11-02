

###bagian modul
import pygame
pygame.init()
import random


###bagian variabel global
lebar_scene = 400
tinggi_scene = 400
judul_scene = "PESAWAT BERBURU"
gambar_belakang = "galaxy.jpg"
gambar_pemain = "rocket.png"
gambar_musuh = "ship_0000.png"
gambar_peluru = "bullet.png"
gambar_rintangan = "asteroid.png"
suara_tembak = "fire.ogg"
suara_belakang = "space.ogg"
GAME_RUN = True #gamenya menyala
GAME_FINISH = False #gamenya masih berjalan
score = 0 #untuk nilai
missed = 0 #untuk yang lewat
jumlah_tembakan = 0 #untuk lacak berapa kali tembak
waktu_reload = 10 #dalam loop


###bagian scene
scene = pygame.display.set_mode((lebar_scene, tinggi_scene))
scene.fill((0,0,0))
pygame.display.set_caption(judul_scene)
belakang = pygame.transform.scale(
   pygame.image.load(gambar_belakang), (lebar_scene, tinggi_scene)
)
fps = pygame.time.Clock()


###bagian musik
pygame.mixer.init()
pygame.mixer.music.load(suara_belakang)
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play()
#efek suara
ciu = pygame.mixer.Sound(suara_tembak)


###bagian tulisan
pygame.font.init()
font1 = pygame.font.SysFont("comic mono", 40)
tulisan_score = font1.render("SCORE:"+str(score), True, (0,0,0))
tulisan_missed = font1.render("MISSED:"+str(missed), True, (0,0,0))
#4
menang = font1.render("WAH HEBAT", True, (0,255,0))
kalah = font1.render("COBA LAGI", True, (255,0,0))


###bagian class
class GameSprite(pygame.sprite.Sprite):
   def __init__(self, gambar, x, y, lebar, tinggi, kecepatan):
       super().__init__()
       self.lebar = lebar
       self.tinggi = tinggi
       self.gambar = pygame.transform.scale(
           pygame.image.load(gambar), (self.lebar, self.tinggi))
       self.kecepatan = kecepatan
       self.rect = self.gambar.get_rect()
       self.rect.x = x
       self.rect.y = y
   def tampil(self):
       scene.blit(self.gambar,(self.rect.x, self.rect.y))
class Player(GameSprite):
   def bergerak(self):
       tombol = pygame.key.get_pressed()
       if tombol[pygame.K_a] and self.rect.x>0: #kekiri
           self.rect.x -= self.kecepatan
       elif tombol[pygame.K_d] and self.rect.x<lebar_scene-self.lebar: #kekanan
           self.rect.x += self.kecepatan
   def tembak(self):
       global jumlah_tembakan
       jumlah_tembakan += 1
       #buat objek peluru
       peluru = Bullet(gambar=gambar_peluru, x=self.rect.centerx,
                       y=self.rect.top, lebar=20, tinggi=40,
                       kecepatan=5)
       grup_peluru.add(peluru)
class Enemy(GameSprite):
   def bergerak(self):
       self.rect.y += self.kecepatan #selalu ke bawah
       #logika untuk pindah ke atas lagi
       global missed #supaya bisa akses miss nya
       if self.rect.y > tinggi_scene:
           self.rect.y = random.randint(-300, -100)
           self.rect.x = random.randint(50, lebar_scene-100)
           missed += 1 #nambah miss nya
class Bullet(GameSprite):
   def bergerak(self):
       self.rect.y -= self.kecepatan #ke atas
       #logika supaya hilang
       if self.rect.y < -100:
           self.kill() #hapus diri sendiri


class Rintangan(GameSprite):
   def bergerak(self):
       self.rect.y += self.kecepatan #selalu ke bawah
       #logika untuk pindah ke atas lagi
       if self.rect.y > tinggi_scene:
           self.rect.y = random.randint(-300, -100)
           self.rect.x = random.randint(50, lebar_scene-100)






###bagian sprite
pemain = Player(gambar=gambar_pemain, x=10, y=tinggi_scene-100,
                   lebar=50, tinggi=50, kecepatan=10)


grup_musuh = pygame.sprite.Group()
jumlah_musuh = 5
for jumlah in range(jumlah_musuh):
   musuh = Enemy(gambar=gambar_musuh, x=random.randint(50,300), y=random.randint(-300, -100),
                   lebar=50, tinggi=50, kecepatan=2)
   grup_musuh.add(musuh)


grup_rintangan = pygame.sprite.Group()
jumlah_rintangan = 2
for jumlah in range(jumlah_rintangan):
   rintangan = Enemy(gambar=gambar_rintangan, x=random.randint(50,300), y=random.randint(-300, -100),
                   lebar=50, tinggi=50, kecepatan=1)
   grup_rintangan.add(rintangan)


grup_peluru = pygame.sprite.Group()


###bagian game loop
while GAME_RUN:
   ##bagian event handler
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           GAME_RUN = False #matikan gamenya
       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE:
               if jumlah_tembakan >= 5 and waktu_reload >= 0:
                   waktu_reload -= 1
               elif jumlah_tembakan >= 5 and waktu_reload <= 0:
                   jumlah_tembakan = 0
                   waktu_reload = 10
               elif jumlah_tembakan <= 5 and waktu_reload >= 10:
                   ciu.play()
                   pemain.tembak()


   ##game masih berjalan
   if GAME_FINISH == False:
       ##tampilkan semua
       scene.blit(belakang, (0,0))
       tulisan_score = font1.render("SCORE:"+str(score), True, (255,255,255))
       tulisan_missed = font1.render("MISSED:"+str(missed), True, (255,255,255))
       scene.blit(tulisan_score, (10, 10))
       scene.blit(tulisan_missed, (200, 10))
       pemain.tampil()
       for rintangan in grup_rintangan:
           rintangan.tampil()
           rintangan.bergerak()
       for musuh in grup_musuh:
           musuh.tampil()
           musuh.bergerak()
       for peluru in grup_peluru:
           peluru.tampil()
           peluru.bergerak()
       #gerakkan semua
       pemain.bergerak()
       #pemeriksaan tabrakan
       if (pygame.sprite.spritecollide(pemain, grup_musuh, False) or
           missed >= 10):
           scene.blit(kalah, (50,50))
           GAME_FINISH = True
       if pygame.sprite.groupcollide(grup_peluru, grup_musuh, True, True):
           score += 1
           #tambah lagi musuh yang hilang, copy dari atas
           musuh = Enemy(gambar=gambar_musuh, x=random.randint(50,300), y=random.randint(-300, -100),
                   lebar=50, tinggi=50, kecepatan=2)
           grup_musuh.add(musuh)
       if pygame.sprite.groupcollide(grup_peluru, grup_rintangan, True, False):
           pass
       if score > 5:
           scene.blit(menang, (50, 50))
           GAME_FINISH = True
          
   ##bagian paling penting
   ##letakkan selalu paling bawah
   fps.tick(60)
   pygame.display.update()

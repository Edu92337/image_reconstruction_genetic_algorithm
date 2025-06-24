import PIL.Image
import numpy as np
import pygame,random,PIL



WIDTH,HEIGHT = 800,800
img = PIL.Image.open('/home/eduardo/Estudos/Projetos/algoritmos_geneticos/paisagem.jpg.webp').convert('RGB').resize((WIDTH, HEIGHT))
CELL_SIZE = 10
GRID_HEIGHT = HEIGHT//CELL_SIZE
GRID_WIDTH = WIDTH//CELL_SIZE


class celula():
    def __init__(self, init_random=True):
        if init_random:
            self.color = [random.randint(0, 255) for _ in range(3)]
        else:
            self.color = [0, 0, 0] 
class Cromossomo():
    def __init__(self, init_random=True):
        self.genoma = [[celula(init_random) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    def show_cromossomo(self, screen):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(screen, self.genoma[i][j].color, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
target_colors = []

for i in range(GRID_HEIGHT):
    linha = []
    for j in range(GRID_WIDTH):
        r_alvo, g_alvo, b_alvo = 0, 0, 0
        count = 0
        for y in range(i*CELL_SIZE, (i+1)*CELL_SIZE):
            for x in range(j*CELL_SIZE, (j+1)*CELL_SIZE):
                r, g, b = img.getpixel((x, y))
                r_alvo += r
                g_alvo += g
                b_alvo += b
                count += 1
        linha.append([r_alvo//count, g_alvo//count, b_alvo//count])
    target_colors.append(linha)    

class GeneticAlgo():
    def __init__(self,number_generations):
        self.population = [Cromossomo() for _ in range(number_generations)]
    
    def fitness(self, cromossomo):
        soma_total = 0
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                r, g, b = cromossomo.genoma[i][j].color
                r_t, g_t, b_t = target_colors[i][j]
               
                soma_total += (r_t - r)**2 + (g_t - g)**2 + (b_t - b)**2
        return 1 / (1 + soma_total) 

    
    def selection(self):
        
        fitnesses = [self.fitness(ind) for ind in self.population]
        total_fitness = sum(fitnesses)
        
        if total_fitness == 0:
            return random.sample(self.population, len(self.population)//2)
        
        
        pais = []
        for _ in range(len(self.population)//2):
            pick = random.uniform(0, total_fitness)
            current = 0
            for i, ind in enumerate(self.population):
                current += fitnesses[i]
                if current > pick:
                    pais.append(ind)
                    break
        return pais
    
    def mutation(self):
        for cromossomo in self.population[1:]:  
            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    if random.random() <= 0.02:
                        for k in range(3):
                            delta = (target_colors[i][j][k] - cromossomo.genoma[i][j].color[k]) // 4
                            cromossomo.genoma[i][j].color[k] = max(0, min(255, 
                                cromossomo.genoma[i][j].color[k] + delta + random.randint(-10, 10)))

    def crossover(self):
        pais = self.selection()
        if len(pais) < 2:
            return
        
        filhos = []
        for i in range(0, len(pais)-1, 2):
            pai1, pai2 = pais[i], pais[i+1]
            filho = Cromossomo(init_random=False)
            
            for x in range(GRID_HEIGHT):
                for y in range(GRID_WIDTH):
                    if random.random() < 0.5:
                        filho.genoma[x][y].color = pai1.genoma[x][y].color.copy()
                    else:
                        filho.genoma[x][y].color = pai2.genoma[x][y].color.copy()
            
            filhos.append(filho)
        
        self.population = pais + filhos

    def run(self, screen):
       
        self.population.sort(key=self.fitness, reverse=True)
        
        elite = self.population[:2]
        
        self.crossover()
        self.mutation()

        self.population = elite + self.population[:-2]
        
        
        self.population[0].show_cromossomo(screen)
        
        



        


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Evolução Genética - Imagem")

    clock = pygame.time.Clock()
    running = True

    ga = GeneticAlgo(number_generations=50)  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        
        ga.run(screen)  
        pygame.display.flip()

        clock.tick(2000) 


      


if __name__ == "__main__":
    main()
# image_reconstruction_genetic_algorithm

This project implements a **Genetic Algorithm (GA)** to approximate a target image using a grid of colored cells. Over successive generations, a population of randomly initialized individuals evolves to closely resemble the original image.

## 🧬 How It Works

Each individual (or chromosome) is a grid of RGB-colored cells. The GA tries to minimize the color difference between each cell and the corresponding region of the original image.

### Genetic Algorithm Steps:

1. **Initialization**  
   - Each chromosome is filled with random colors.  
   - The target image is resized and divided into a grid based on `CELL_SIZE`.

2. **Fitness Evaluation**  
   - The fitness function calculates the sum of squared differences between the RGB values of each cell and the average color of the corresponding region in the target image.

3. **Selection**  
   - Roulette wheel selection is used to choose parents, giving preference to individuals with higher fitness.

4. **Crossover**  
   - A uniform crossover combines two parent chromosomes by randomly selecting cells from each to form a new child.

5. **Mutation**  
   - A small mutation rate causes slight changes in the color of some cells, nudging them toward the target region's color with added randomness.

6. **Elitism**  
   - The best individuals are preserved in the next generation to maintain progress.

7. **Visualization**  
   - Pygame displays the best chromosome of each generation in real time.

---

## 🖼 Image Input

Make sure to specify the path to the target image in the script:



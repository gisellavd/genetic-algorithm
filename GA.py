import math
import random

# batas nilai minimum dan maksimum untuk variabel x dan y
min_val = -5
max_val = 5

# panjang kromosom
m = 10

# banyaknya kromosom dalam 1 populasi
n = 5

# probabilitas crossover dan mutasi
pc = 0.8
pm = 0.03

# maksimum generasi
genmax = 20



# Membuat chromosome (binary encoding menggunakan m/2 bit atau m/2 gen)
def chromosome(m):
  chrom = []
  for i in range(m):
    chrom.append(random.randint(0, 1))
  return chrom

# Membuat Populasi
def createPopulation(n, m):
  pop = []
  for i in range(n):
    pop.append(chromosome(m))
  return pop

# Membagi genotype menjadi 2 bagian
def split(chrom):
  s = m // 2
  return chrom[:s], chrom[s:]

# Decode kromosom
def decode(geno, min_val, max_val):
  a = 0
  b = 0
  for i in range(len(geno)):
    gen = geno[i]
    a += (gen * (2 ** -(i+1))) # rumus
    b += (2 ** -(i+1))
  val = min_val + ((max_val - min_val) * a)/b
  return val

# Fungsi yang ingin dicari nilai minimumnya
def fungsi(x, y):
  h = ((math.cos(x) + math.sin(y))**2)/((x**2)+(y**2))
  return h

# Nilai fitness
def fitness(h):
  f = 1/(h + 0.001)
  return f

def createFitnessList(pop):
  fitPop = []
  for i in range(len(pop)):
    g_x, g_y = split(pop[i])
    x = decode(g_x, min_val, max_val)
    y = decode(g_y, min_val, max_val)
    fitPop.append(fitness(fungsi(x, y)))
  return fitPop

# Pemilihan orangtua: Tournament Selection
def tournamentSelection(pop):
  best = []
  for i in range(3):
    best.append(pop[random.randint(0, len(pop)-1)])
  fitBest = createFitnessList(best)
  fitMax = fitBest[0]
  fitScndMax = fitBest[0]
  idxMax = 0
  idxScndMax = 0
  for i in range(len(fitBest)):
    if fitBest[i] > fitMax:
      fitMax = fitBest[i]
      idxMax = i
  for i in range(len(fitBest)):
    if fitBest[i] > fitScndMax and fitBest[i] != fitMax:
      fitScndMax = fitBest[i]
      idxScndMax = i
  idxPar1 = idxMax
  idxPar2 = idxScndMax
  return best[idxPar1], best[idxPar2]

# 1-point crossover
def crossover(par1, par2, pc):
  child1 = par1.copy()
  child2 = par2.copy()
  r = random.random()
  if (r <= pc):
    pt = random.randint(1, len(par1)-1)
    print("Crossover - Titik potong:", pt)
    child1 = par1[:pt] + par2[pt:]
    child2 = par2[:pt] + par1[pt:]
  else:
    child1 = par1
    child2 = par2
  return child1, child2

# mutasi: membalik bit
def mutation(chrom, pm):
  tm = []
  for i in range(len(chrom)):
    r = random.random()
    if r <= pm:
      tm.append(i+1)
      if chrom[i] == 0:
        chrom[i] = 1
      else:
        chrom[i] = 0
  if tm:
    print("Posisi mutasi:", tm)
  return chrom

# seleksi survivor: dengan elitisme
def elitism(pop):
  newPop = []
  fitPop = createFitnessList(pop)
  fitmax = fitPop[0]
  idxmax = 0
  for i in range(len(fitPop)):
    if fitPop[i] > fitmax:
      fitmax = fitPop[i]
      idxmax = i
  newPop.append(pop[idxmax])
  return newPop

pop = createPopulation(n, m)
gen = 1
while (gen < genmax):
  print("Generasi ke-", gen)
  print("Populasi: ", pop)
  newPop = elitism(pop)
  while (len(newPop) < len(pop)):
    parent1, parent2 = tournamentSelection(pop)
    print("Parent 1: ", parent1)
    print("Parent 2: ", parent2)
    child1, child2 = crossover(parent1, parent2, pc)
    child1 = mutation(child1, pm)
    child2 = mutation(child2, pm)
    print("Child 1: ", child1)
    print("Child 2: ", child2)
    newPop.append(child1)
    if len(newPop) < len(pop):
      newPop.append(child2)
  pop = newPop # Generational Replacement
  fitnessPop = createFitnessList(pop)
  gen += 1
  print()
print("Generasi ke-", gen)
print("Populasi: ", pop)
# Mencari kromosom terbaik
fitmax = fitnessPop[0]
idxmax = 0
for i in range(len(fitnessPop)):
  if fitnessPop[i] > fitmax:
    fitmax = fitnessPop[i]
    idxmax = i
print()
print("Banyak generasi: ", gen)
print("Kromosom terbaik: ", pop[idxmax])
g_x, g_y = split(pop[idxmax])
x = decode(g_x, min_val, max_val)
y = decode(g_y, min_val, max_val)
print("Dengan")
print("Nilai x: ", x)
print("Nilai y: ", y)
print("Nilai Fitness: ", fitnessPop[idxmax])
print("Nilai Fungsi: ", fungsi(x, y))
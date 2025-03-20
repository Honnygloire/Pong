import pygame
import random

# Initialisation de pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Dimensions de la fenêtre
LARGEUR_FENETRE = 600
HAUTEUR_FENETRE = 400
TAILLE_BALLE = 15
TAILLE_RAQUETTE = 10
VITESSE_RAQUETTE = 10
SCORE_LIMITE = 5  # Score pour gagner

# Création de la fenêtre
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Pong")

# Fonction pour afficher du texte centré
def afficher_texte(texte, taille, couleur, y):
    font = pygame.font.SysFont("Arial", taille)
    texte_surface = font.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect(center=(LARGEUR_FENETRE // 2, y))
    fenetre.blit(texte_surface, texte_rect)  


# Fonction pour demander le nom des joueurs
def saisir_nom(joueur):
    texte = ""
    actif = True
    while actif:
        fenetre.fill(NOIR)
        afficher_texte(f"Nom du {joueur} :", 30, BLANC, 150)
        afficher_texte(texte, 30, ROUGE, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and texte.strip():
                    return texte.strip()
                elif event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]
                elif len(texte) < 10:
                    texte += event.unicode

# Menu principal
def menu():
    while True:
        fenetre.fill(NOIR)
        afficher_texte("PONG", 50, BLANC, 100)
        afficher_texte("1. Jouer contre l'ordinateur", 30, BLANC, 200)
        afficher_texte("2. Jouer à 2 joueurs", 30, BLANC, 250)
        afficher_texte("Appuyez sur 1 ou 2 pour choisir", 25, ROUGE, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "solo", saisir_nom("joueur")
                elif event.key == pygame.K_2:
                    return "multi", saisir_nom("joueur 1"), saisir_nom("joueur 2")

# Fonction principale du jeu
def jeu(mode, nom_joueur1, nom_joueur2="Ordinateur"):
    # Positions initiales
    x_balle, y_balle = LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2
    vitesse_x_balle, vitesse_y_balle = 4 * random.choice((1, -1)), 4 * random.choice((1, -1))

    x_raquette_gauche, y_raquette_gauche = 20, HAUTEUR_FENETRE // 2 - 30
    x_raquette_droite, y_raquette_droite = LARGEUR_FENETRE - 30, HAUTEUR_FENETRE // 2 - 30

    score_gauche, score_droite = 0, 0
    clock = pygame.time.Clock()
    jeu_en_cours = True

    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jeu_en_cours = False

        # Vérifier la victoire
        if score_gauche >= SCORE_LIMITE or score_droite >= SCORE_LIMITE:
            jeu_en_cours = False
            gagnant = nom_joueur1 if score_gauche >= SCORE_LIMITE else nom_joueur2
            fenetre.fill(NOIR)
            afficher_texte(f"{gagnant} a gagné !", 40, ROUGE, HAUTEUR_FENETRE // 2)
            pygame.display.update()
            pygame.time.delay(3000)
            break

        # Contrôles des raquettes
        touches = pygame.key.get_pressed()

        if mode == "multi":
            # Joueur 1 (gauche) : W/S
            if touches[pygame.K_w] and y_raquette_gauche > 0:
                y_raquette_gauche -= VITESSE_RAQUETTE
            if touches[pygame.K_s] and y_raquette_gauche < HAUTEUR_FENETRE - 60:
                y_raquette_gauche += VITESSE_RAQUETTE

            # Joueur 2 (droite) : flèches ↑/↓
            if touches[pygame.K_UP] and y_raquette_droite > 0:
                y_raquette_droite -= VITESSE_RAQUETTE
            if touches[pygame.K_DOWN] and y_raquette_droite < HAUTEUR_FENETRE - 60:
                y_raquette_droite += VITESSE_RAQUETTE
        else:
            # Joueur (gauche) : flèches ↑/↓
            if touches[pygame.K_UP] and y_raquette_gauche > 0:
                y_raquette_gauche -= VITESSE_RAQUETTE
            if touches[pygame.K_DOWN] and y_raquette_gauche < HAUTEUR_FENETRE - 60:
                y_raquette_gauche += VITESSE_RAQUETTE

            # IA (droite)
            if y_raquette_droite + 30 < y_balle:
                y_raquette_droite += min(VITESSE_RAQUETTE, HAUTEUR_FENETRE - 60 - y_raquette_droite)
            elif y_raquette_droite + 30 > y_balle:
                y_raquette_droite -= min(VITESSE_RAQUETTE, y_raquette_droite)

        # Mouvement de la balle
        x_balle += vitesse_x_balle
        y_balle += vitesse_y_balle

        # Collision avec le plafond ou le sol
        if y_balle <= 0 or y_balle >= HAUTEUR_FENETRE - TAILLE_BALLE:
            vitesse_y_balle = -vitesse_y_balle

        # Collision avec les raquettes
        if (x_balle <= x_raquette_gauche + TAILLE_RAQUETTE and y_raquette_gauche < y_balle < y_raquette_gauche + 60) or \
           (x_balle >= x_raquette_droite - TAILLE_BALLE and y_raquette_droite < y_balle < y_raquette_droite + 60):
            vitesse_x_balle = -vitesse_x_balle

        # Point marqué
        if x_balle <= 0:
            score_droite += 1
            x_balle, y_balle = LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2
        if x_balle >= LARGEUR_FENETRE - TAILLE_BALLE:
            score_gauche += 1
            x_balle, y_balle = LARGEUR_FENETRE // 2, HAUTEUR_FENETRE // 2

        # Effacer l'écran
        fenetre.fill(NOIR)

        # Affichage des scores et des noms
        afficher_texte(f"{nom_joueur1} : {score_gauche}", 25, ROUGE, 20)
        afficher_texte(f"{nom_joueur2} : {score_droite}", 25, ROUGE, 50)

        # Dessiner balle et raquettes
        pygame.draw.rect(fenetre, BLANC, (x_balle, y_balle, TAILLE_BALLE, TAILLE_BALLE))
        pygame.draw.rect(fenetre, BLANC, (x_raquette_gauche, y_raquette_gauche, TAILLE_RAQUETTE, 60))
        pygame.draw.rect(fenetre, BLANC, (x_raquette_droite, y_raquette_droite, TAILLE_RAQUETTE, 60))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Lancer le jeu
selection = menu()
jeu(*selection)

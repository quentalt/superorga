import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import yaml
import os


# Fonction pour charger le YAML
def load_hierarchy(yml_file):
    if not os.path.exists(yml_file):
        raise FileNotFoundError(f"Le fichier {yml_file} n'a pas été trouvé.")

    with open(yml_file, 'r') as file:
        data = yaml.safe_load(file)
        settings = data.get('settings', {})
        levels = data.get('levels', [])
        connections = data.get('connections', [])
        if not levels:
            raise ValueError("Le fichier YAML doit contenir au moins un niveau.")
        return settings, levels, connections


# Fonction pour afficher les images
def get_image(path, zoom=0.15):
    if os.path.exists(path):
        img = plt.imread(path)
        return OffsetImage(img, zoom=zoom)
    else:
        raise FileNotFoundError(f"L'image {path} n'a pas été trouvée.")


# Fonction pour dessiner la hiérarchie avec les images
def draw_hierarchy(settings, levels, connections):
    fig, ax = plt.subplots(figsize=(8, 10))

    # Paramètres de personnalisation
    arrow_color = settings.get('arrow_color', 'black')
    arrow_style = settings.get('arrow_style', 'arrow')
    arrow_width = settings.get('arrow_width', 2)
    frame_color = settings.get('frame_color', 'black')
    frame_width = settings.get('frame_width', 2)
    text_color = settings.get('text_color', 'black')
    text_size = settings.get('text_size', 14)
    text_font = settings.get('text_font', 'Arial')
    image_zoom = settings.get('image_zoom', 0.15)

    # Calcul des positions en fonction des niveaux
    num_levels = len(levels)
    y_positions = [1 - (i + 1) / (num_levels + 1) for i in range(num_levels)]

    positions = {}

    for level_idx, level in enumerate(levels):
        grades = level['grades']
        num_grades = len(grades)

        # Calcul des positions pour chaque grade au sein d'un niveau
        x_positions = [(i + 1) / (num_grades + 1) for i in range(num_grades)]
        curr_positions = [(x, y_positions[level_idx]) for x in x_positions]

        for grade_idx, grade in enumerate(grades):
            title = grade['title']
            subtitle = grade.get('subtitle', '')
            img = get_image(grade['image'], zoom=image_zoom)
            pos = curr_positions[grade_idx]

            positions[title] = pos  # Stocker la position pour les connexions
            ab = AnnotationBbox(img, pos, frameon=True, bboxprops=dict(edgecolor=frame_color, linewidth=frame_width))
            ax.add_artist(ab)
            ax.text(pos[0], pos[1] - 0.1, title, ha='center', va='center', fontsize=text_size, fontweight='bold',
                    color=text_color, fontname=text_font)
            if subtitle:
                ax.text(pos[0], pos[1] - 0.15, subtitle, ha='center', va='center', fontsize=text_size * 0.8,
                        color=text_color)

        # Connexion horizontale entre grades si demandé
        if level.get('connect_horizontal', False) and len(curr_positions) > 1:
            for j in range(len(curr_positions) - 1):
                ax.plot([curr_positions[j][0], curr_positions[j + 1][0]],
                        [curr_positions[j][1], curr_positions[j + 1][1]],
                        color=arrow_color, lw=arrow_width)

        # Connexion verticale vers un niveau inférieur
        if level.get('connect_vertical', False) and len(curr_positions) > 0:
            for pos in curr_positions:
                middle_x = pos[0]
                ax.plot([middle_x, middle_x], [pos[1], pos[1] - (1 / (num_levels + 1))], color=arrow_color,
                        lw=arrow_width)

    # Dessiner les connexions explicites
    for connection in connections:
        from_grade = connection['from']
        to_grades = connection['to']
        from_pos = positions.get(from_grade)

        if from_pos:
            for to_grade in to_grades:
                to_pos = positions.get(to_grade)
                if to_pos:
                    if arrow_style == 'arrow':
                        ax.annotate('', xy=to_pos, xytext=from_pos,
                                    arrowprops=dict(arrowstyle="->", lw=arrow_width, color=arrow_color))
                    else:
                        ax.plot([from_pos[0], to_pos[0]], [from_pos[1], to_pos[1]],
                                color=arrow_color, lw=arrow_width)

    # Paramètres de l'affichage
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')  # On cache les axes

    # Afficher le diagramme
    plt.tight_layout()
    plt.show()


# Option pour sauvegarder le diagramme
def save_hierarchy(settings, levels, connections, filename='hierarchy.png'):
    draw_hierarchy(settings, levels, connections)
    plt.savefig(filename, bbox_inches='tight')
    print(f"Le diagramme a été sauvegardé sous {filename}")


# Charger la hiérarchie depuis le fichier YAML
settings, levels, connections = load_hierarchy('hierarchie.yml')

# Dessiner la hiérarchie
draw_hierarchy(settings, levels, connections)

# Sauvegarder le diagramme (optionnel)
# save_hierarchy(settings, levels, connections, filename='organigramme.png')

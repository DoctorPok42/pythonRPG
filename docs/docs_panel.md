# Panel Documentation (PythonRPG)

L'affichage du jeu utilise en partie les panels de la librairie python Rich et ici les panels sont géré sous forme de classe

Voici les méthodes implémanté dans la classe <span style="color:magenta">Panels</span> :

<span style="color:green">

constructeur()  
create_panel()  
display_panel()  
update_panel_text(<span style="color:lightblue">text</span>)  
update_panel_title(<span style="color:lightblue">title</span>)  
update_panel_subtitle(<span style="color:lightblue">subtitle</span>)  

</span>

### Constructeur

Le constructeur a besoin de plusieurs arguments :

- <span style="color:orange">**text**</span> : string correspondant au contenu du panel
-  <span style="color:orange">**title**</span> : string correspondant au titre du panel
- <span style="color:orange">**padding**</span> : tuple de 2 int correspondant à la marge interne du panel
- <span style="color:orange">**subtitle**</span> : string corespondant au titre secondaire du panel
- <span style="color:orange">**border**</span> : string correspondant à la couleur de la bodure du panel

Dans votre code vous devrez créer votre instance de la classe Panels de cette manière :
```python
from panel import Panels

panel_name = Panels(text, title, padding, subtitle, border) 
```

### Create Panel

La méthode create_panel() permet de créer le panel en fonction des valeurs qui ont été donné dans le constructeur plus tôt

Pour l'utiliser dans votre code vous devez déjà avoir déclaré une instance de la classe Panel et ensuite faire ceci :

```python
panel_name.create_panel()
```
### Display Panel

La méthode display_panel() permet d'afficher le panel

Voici comment l'utiliser dans le code :

```python
panel_name.display_panel()
```

### Update Panel Text

La méthode <span style="color:green">update_panel_text(<span style="color:lightblue">text</span>)</span> permet de changer le contenu du panel avec le texte fourni

Voici coment l'utiliser :

```python
panel_name.update_panel_name(text)
```

### Update Panel Title

La méthode <span style="color:green">update_panel_title(<span style="color:lightblue">title</span>)</span> permet de changer le titre du panel avec le texte fourni

Voici coment l'utiliser :

```python
panel_name.update_panel_title(subtitle)
```

### Update Panel Subtitle

La méthode <span style="color:green">update_panel_subtitle(<span style="color:lightblue">subtitle</span>)</span> permet de changer le sous-titre du panel avec le texte fourni

Voici coment l'utiliser :

```python
panel_name.update_panel_subtitle(title)
```

<span style="color:grey">Documentation créé par Lytzeer</span>
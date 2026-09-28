Attribute VB_Name = "YebaAnimations"
' =====================================================================================
'  YEBA FORMATIONS — Soirée de lancement
'  Module VBA PowerPoint : Morphose + animations d'entrée automatiques
'
'  INSTALLATION (PowerPoint Windows ou Mac, Microsoft 365 / 2019 et plus pour la Morphose) :
'    1. Ouvrir dist/YEBA_Soiree_Lancement.pptx
'    2. Alt + F11  →  Fichier  →  Importer un fichier…  →  choisir ce fichier .bas
'    3. Alt + F8   →  lancer « YebaToutAppliquer »
'    4. Enregistrer sous  →  Présentation PowerPoint (*.pptx)  (la macro n'a pas besoin
'       d'être conservée : les effets restent dans le fichier)
'
'  PRINCIPE : les effets sont posés d'après le NOM des objets (volet Sélection, Alt + F10),
'  noms générés par pptx/build_pptx.py. Les objets « !!xxx » présents sur deux slides
'  consécutives sont animés par la Morphose : on ne leur ajoute pas d'effet d'entrée.
'
'  Aucune donnée n'est envoyée hors de votre poste : tout s'exécute localement.
' =====================================================================================

Private Const DELAI_ECHELON As Single = 0.2

' ------------------------------------------------------------------ point d'entrée
Public Sub YebaToutAppliquer()
    YebaMorphosePartout
    YebaAppliquerAnimations
    YebaVideoAutomatique
    MsgBox "Morphose et animations appliquées sur " & ActivePresentation.Slides.Count & " slides." & vbCrLf & _
           "Lancez « YebaVerifierAccessibilite » pour contrôler les tailles de texte.", vbInformation, "YEBA FORMATIONS"
End Sub

' ------------------------------------------------------------------ transitions
Public Sub YebaMorphosePartout()
    Dim sld As Slide
    For Each sld In ActivePresentation.Slides
        With sld.SlideShowTransition
            On Error Resume Next
            If ContientTexte(sld, "!!yeba", "Y") Then
                .EntryEffect = ppEffectMorphByChar      ' YEBA → Y : les lettres E, B, A s'effacent
            Else
                .EntryEffect = ppEffectMorphByObject
            End If
            If Err.Number <> 0 Then                   ' PowerPoint sans Morphose : repli en fondu
                Err.Clear
                .EntryEffect = ppEffectFadeSmoothly
            End If
            On Error GoTo 0
            .Duration = 1.5
            .AdvanceOnClick = msoTrue
        End With
    Next sld
End Sub

' ------------------------------------------------------------------ animations d'entrée
Public Sub YebaAppliquerAnimations()
    Dim sld As Slide, shp As Shape, seq As Sequence
    For Each sld In ActivePresentation.Slides
        Set seq = sld.TimeLine.MainSequence
        ViderSequence seq
        For Each shp In sld.Shapes
            AnimerForme sld, seq, shp
        Next shp
    Next sld
End Sub

Public Sub YebaRetirerAnimations()
    Dim sld As Slide
    For Each sld In ActivePresentation.Slides
        ViderSequence sld.TimeLine.MainSequence
    Next sld
End Sub

Private Sub AnimerForme(sld As Slide, seq As Sequence, shp As Shape)
    Dim nom As String, e As Effect
    nom = shp.Name

    ' Objets pris en charge par la Morphose ou décoratifs : aucun effet d'entrée
    If Commence(nom, "!!logo") Or Commence(nom, "!!ag") Or Commence(nom, "!!marqueur") _
       Or Commence(nom, "!!barre") Or Commence(nom, "!!tuile") Or Commence(nom, "!!code") _
       Or Commence(nom, "!!droite") Or Commence(nom, "!!embleme") Or Commence(nom, "!!yeba") _
       Or Commence(nom, "guillemets") Or Commence(nom, "legende") Or Commence(nom, "!!filigrane") _
       Or Commence(nom, "!!video") Or Commence(nom, "meta") Then Exit Sub

    Select Case True
        Case Commence(nom, "kicker"), Commence(nom, "famille")
            Ajouter seq, shp, msoAnimEffectFade, msoAnimTriggerAfterPrevious, 0, 0.5

        Case Commence(nom, "!!titre")
            ' Titre en deux temps : ligne blanche puis ligne or (effet « chute » de la phrase)
            Set e = Ajouter(seq, shp, msoAnimEffectFade, msoAnimTriggerAfterPrevious, 0.1, 0.7, msoAnimateTextByFirstLevel)
            EnchainerParagraphes seq, shp, 0.6

        Case Commence(nom, "!!carte"), Commence(nom, "!!badge"), Commence(nom, "!!format-")
            Ajouter seq, shp, msoAnimEffectAscend, msoAnimTriggerAfterPrevious, DELAI_ECHELON, 0.5
        Case Commence(nom, "!!photo"), Commence(nom, "nom"), Commence(nom, "role")
            Ajouter seq, shp, msoAnimEffectFade, msoAnimTriggerWithPrevious, 0, 0.5

        Case Commence(nom, "!!num")
            ' Valeurs : une par clic, pour laisser l'orateur la commenter
            Ajouter seq, shp, msoAnimEffectZoom, msoAnimTriggerOnPageClick, 0, 0.4
        Case Commence(nom, "!!val")
            Ajouter seq, shp, msoAnimEffectFade, msoAnimTriggerWithPrevious, 0.1, 0.5

        Case Commence(nom, "!!pilier"), Commence(nom, "detail"), Commence(nom, "!!trait")
            Ajouter seq, shp, msoAnimEffectAscend, msoAnimTriggerAfterPrevious, 0.05, 0.4

        Case Commence(nom, "!!ligne")
            Set e = Ajouter(seq, shp, msoAnimEffectWipe, msoAnimTriggerAfterPrevious, 0.2, 1.4)
            e.EffectParameters.Direction = msoAnimDirectionLeft
        Case Commence(nom, "!!jalon"), Commence(nom, "date"), Commence(nom, "etape")
            Ajouter seq, shp, msoAnimEffectFade, msoAnimTriggerAfterPrevious, 0.05, 0.35

        Case Commence(nom, "!!baobab")
            Set e = Ajouter(seq, shp, msoAnimEffectWipe, msoAnimTriggerAfterPrevious, 0.2, 1.6)
            e.EffectParameters.Direction = msoAnimDirectionBottom
        Case Commence(nom, "illustration")
            Ajouter seq, shp, msoAnimEffectWheel, msoAnimTriggerAfterPrevious, 0.2, 1.2

        Case Commence(nom, "puce")
            Ajouter seq, shp, msoAnimEffectFly, msoAnimTriggerAfterPrevious, 0.1, 0.45
        Case Commence(nom, "chip")
            Ajouter seq, shp, msoAnimEffectZoom, msoAnimTriggerAfterPrevious, 0.05, 0.3

        Case Commence(nom, "branche"), Commence(nom, "sous-"), Commence(nom, "mots"), _
             Commence(nom, "traduction"), Commence(nom, "explication"), Commence(nom, "titre-droite")
            Ajouter seq, shp, msoAnimEffectFade, msoAnimTriggerAfterPrevious, 0.3, 0.6

        Case Commence(nom, "!!live")
            ' Pastille « LIVE » : pulsation continue
            Set e = Ajouter(seq, shp, msoAnimEffectFlashBulb, msoAnimTriggerAfterPrevious, 0, 0.8)
            e.Timing.RepeatCount = 30
    End Select
End Sub

' ------------------------------------------------------------------ vidéo d'intro
Public Sub YebaVideoAutomatique()
    Dim sld As Slide, shp As Shape
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If Commence(shp.Name, "!!video") Then
                With shp.AnimationSettings.PlaySettings
                    .PlayOnEntry = msoTrue
                    .LoopUntilStopped = msoTrue
                    .HideWhileNotPlaying = msoFalse
                End With
            End If
        Next shp
    Next sld
End Sub

' ------------------------------------------------------------------ accessibilité
' Signale tout texte visible inférieur à 24 pt (public malvoyant : charte YEBA).
Public Sub YebaVerifierAccessibilite()
    Dim sld As Slide, shp As Shape, i As Long, rapport As String, n As Long
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If shp.HasTextFrame Then
                If shp.TextFrame.HasText Then
                    For i = 1 To shp.TextFrame.TextRange.Runs.Count
                        With shp.TextFrame.TextRange.Runs(i)
                            If Len(Trim(.Text)) > 0 And .Font.Size < 24 Then
                                n = n + 1
                                rapport = rapport & "Slide " & sld.SlideIndex & " — « " & Left(.Text, 30) & " » : " & .Font.Size & " pt" & vbCrLf
                            End If
                        End With
                    Next i
                End If
            End If
        Next shp
    Next sld
    If n = 0 Then
        MsgBox "Aucun texte sous 24 pt. Présentation conforme à la règle de lisibilité YEBA.", vbInformation, "Accessibilité"
    Else
        MsgBox n & " passage(s) sous 24 pt :" & vbCrLf & vbCrLf & rapport, vbExclamation, "Accessibilité"
    End If
End Sub

' ------------------------------------------------------------------ outils
Private Function Ajouter(seq As Sequence, shp As Shape, effet As MsoAnimEffect, declencheur As MsoAnimTriggerType, _
                         delai As Single, duree As Single, Optional niveau As MsoAnimateByLevel = msoAnimateLevelNone) As Effect
    Dim e As Effect
    Set e = seq.AddEffect(Shape:=shp, effectId:=effet, Level:=niveau, trigger:=declencheur)
    e.Timing.Duration = duree
    e.Timing.TriggerDelayTime = delai
    Set Ajouter = e
End Function

' Les paragraphes suivants d'un titre s'enchaînent automatiquement (pas de clic supplémentaire)
Private Sub EnchainerParagraphes(seq As Sequence, shp As Shape, delai As Single)
    Dim i As Long, premier As Boolean
    premier = True
    For i = 1 To seq.Count
        If seq(i).Shape.Name = shp.Name Then
            If Not premier Then
                seq(i).Timing.TriggerType = msoAnimTriggerAfterPrevious
                seq(i).Timing.TriggerDelayTime = delai
            End If
            premier = False
        End If
    Next i
End Sub

Private Sub ViderSequence(seq As Sequence)
    Dim i As Long
    For i = seq.Count To 1 Step -1
        seq(i).Delete
    Next i
End Sub

Private Function Commence(texte As String, prefixe As String) As Boolean
    Commence = (Left$(texte, Len(prefixe)) = prefixe)
End Function

Private Function ContientTexte(sld As Slide, nom As String, valeur As String) As Boolean
    Dim shp As Shape
    For Each shp In sld.Shapes
        If shp.Name = nom Then
            If shp.HasTextFrame Then
                If Trim$(shp.TextFrame.TextRange.Text) = valeur Then ContientTexte = True
            End If
        End If
    Next shp
End Function

Attribute VB_Name = "YebaAnimations"
' =====================================================================================
'  YEBA FORMATIONS — « YEBA — Saison 1 » (soirée de lancement)
'  Module VBA PowerPoint v2 : contrôle, mode sobre / cinéma, nettoyage avant envoi
'
'  IMPORTANT (v2) : les animations, la Morphose, la lecture automatique des vidéos et l'avance
'  automatique après le générique sont DÉJÀ dans le fichier (générés par pptx/build_pptx.py).
'  Cette macro ne les efface jamais. Elle sert à :
'    • YebaVerifier            : rapport complet (Morphose, vidéos, textes < 24 pt, texte alternatif,
'                                 post-it « à confirmer », slides masquées) — à lancer avant la soirée ;
'    • YebaModeSobre           : fonds vidéo figés sur leur image (PC modeste, public sensible au mouvement) ;
'    • YebaModeCinema          : fonds vidéo relancés en boucle, muets ;
'    • YebaRetirerPostIt       : supprime les post-it rouges hors champ avant d'envoyer le fichier ;
'    • YebaMorphosePartout     : remet la Morphose sur les slides ajoutées à la main (sans toucher
'                                 à l'avance automatique des vidéos).
'
'  INSTALLATION (Microsoft 365 / PowerPoint 2019 et plus pour la Morphose) :
'    1. Ouvrir dist/YEBA_Soiree_Lancement.pptx
'    2. Alt + F11  →  Fichier  →  Importer un fichier…  →  choisir ce fichier .bas
'    3. Alt + F8   →  lancer « YebaVerifier »
'    4. Enregistrer au format .pptx (la macro n'a pas besoin d'être conservée)
'
'  Aucune donnée n'est envoyée hors de votre poste : tout s'exécute localement.
' =====================================================================================

Private Const NOM_FOND As String = "fond-video"
Private Const NOM_POSTIT As String = "a-confirmer"

' ------------------------------------------------------------------ rapport de contrôle
Public Sub YebaVerifier()
    Dim sld As Slide, shp As Shape, i As Long
    Dim petits As Long, sansAlt As Long, postits As Long, masquees As Long, videos As Long, sansMorph As Long
    Dim detail As String

    For Each sld In ActivePresentation.Slides
        If sld.SlideShowTransition.Hidden = msoTrue Then masquees = masquees + 1
        If Not EstMorphose(sld.SlideShowTransition.EntryEffect) Then sansMorph = sansMorph + 1
        For Each shp In sld.Shapes
            If shp.Name = NOM_POSTIT Then
                postits = postits + 1
                detail = detail & "• Slide " & sld.SlideIndex & " : post-it « à confirmer »" & vbCrLf
            End If
            If shp.Type = msoMedia Then videos = videos + 1
            ' Texte alternatif : obligatoire sur les images porteuses de sens (calques décoratifs exclus)
            If shp.Type = msoPicture Then
                If Len(Trim$(shp.AlternativeText)) = 0 And Not EstDecoratif(shp.Name) Then
                    sansAlt = sansAlt + 1
                    detail = detail & "• Slide " & sld.SlideIndex & " : image « " & shp.Name & " » sans texte alternatif" & vbCrLf
                End If
            End If
            ' Lisibilité : aucun texte projeté sous 24 pt (public malvoyant, charte YEBA)
            If shp.HasTextFrame And shp.Name <> NOM_POSTIT Then
                If shp.TextFrame.HasText Then
                    For i = 1 To shp.TextFrame.TextRange.Runs.Count
                        With shp.TextFrame.TextRange.Runs(i)
                            If Len(Trim$(.Text)) > 0 And .Font.Size < 20 Then
                                petits = petits + 1
                                detail = detail & "• Slide " & sld.SlideIndex & " : « " & Left$(.Text, 28) & " » en " & .Font.Size & " pt" & vbCrLf
                            End If
                        End With
                    Next i
                End If
            End If
        Next shp
    Next sld

    MsgBox "Slides : " & ActivePresentation.Slides.Count & " (dont " & masquees & " masquées : épisodes 5 à 7)" & vbCrLf & _
           "Vidéos intégrées : " & videos & vbCrLf & _
           "Slides sans Morphose : " & sansMorph & IIf(sansMorph > 0, "  → lancer YebaMorphosePartout", "") & vbCrLf & _
           "Textes trop petits : " & petits & vbCrLf & _
           "Images sans texte alternatif : " & sansAlt & vbCrLf & _
           "Post-it « à confirmer » : " & postits & IIf(postits > 0, "  → à traiter puis YebaRetirerPostIt", "") & vbCrLf & vbCrLf & _
           IIf(Len(detail) > 0, detail, "Rien à signaler."), _
           IIf(petits + sansAlt + postits + sansMorph = 0, vbInformation, vbExclamation), "YEBA — contrôle avant soirée"
End Sub

' ------------------------------------------------------------------ fonds vidéo
' Mode sobre : chaque fond vidéo reste affiché sur son image fixe et ne se lance plus.
Public Sub YebaModeSobre()
    Dim n As Long
    n = ReglerFonds(False)
    MsgBox n & " fond(s) vidéo figé(s) sur leur image. Le générique, les épisodes et les clips restent inchangés.", _
           vbInformation, "YEBA — mode sobre"
End Sub

' Mode cinéma : chaque fond vidéo démarre seul, en boucle, sans son.
Public Sub YebaModeCinema()
    Dim n As Long
    n = ReglerFonds(True)
    MsgBox n & " fond(s) vidéo en lecture automatique, en boucle et muets.", vbInformation, "YEBA — mode cinéma"
End Sub

Private Function ReglerFonds(lecture As Boolean) As Long
    Dim sld As Slide, shp As Shape, i As Long, seq As Sequence
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            If shp.Name = NOM_FOND And shp.Type = msoMedia Then
                ReglerFonds = ReglerFonds + 1
                On Error Resume Next
                shp.MediaFormat.Muted = True
                On Error GoTo 0
                If lecture Then
                    With shp.AnimationSettings.PlaySettings
                        .PlayOnEntry = msoTrue
                        .LoopUntilStopped = msoTrue
                        .HideWhileNotPlaying = msoFalse
                    End With
                Else
                    Set seq = sld.TimeLine.MainSequence
                    For i = seq.Count To 1 Step -1
                        If seq(i).Shape.Name = NOM_FOND Then seq(i).Delete
                    Next i
                    With shp.AnimationSettings.PlaySettings
                        .PlayOnEntry = msoFalse
                        .LoopUntilStopped = msoFalse
                        .HideWhileNotPlaying = msoFalse
                    End With
                End If
            End If
        Next shp
    Next sld
End Function

' ------------------------------------------------------------------ avant envoi du fichier
Public Sub YebaRetirerPostIt()
    Dim sld As Slide, i As Long, n As Long
    For Each sld In ActivePresentation.Slides
        For i = sld.Shapes.Count To 1 Step -1
            If sld.Shapes(i).Name = NOM_POSTIT Then
                sld.Shapes(i).Delete
                n = n + 1
            End If
        Next i
    Next sld
    MsgBox n & " post-it supprimé(s).", vbInformation, "YEBA"
End Sub

' ------------------------------------------------------------------ Morphose
' Remet la Morphose (repli : fondu) sans toucher à l'avance automatique des slides vidéo.
Public Sub YebaMorphosePartout()
    Dim sld As Slide, garderAuto As Boolean, delai As Single
    For Each sld In ActivePresentation.Slides
        With sld.SlideShowTransition
            garderAuto = (.AdvanceOnTime = msoTrue)
            delai = .AdvanceTime
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
            .AdvanceOnClick = msoTrue
            If garderAuto Then
                .AdvanceOnTime = msoTrue
                .AdvanceTime = delai
            End If
        End With
    Next sld
    MsgBox "Morphose vérifiée sur " & ActivePresentation.Slides.Count & " slides.", vbInformation, "YEBA"
End Sub

' ------------------------------------------------------------------ outils
Private Function EstMorphose(effet As PpEntryEffect) As Boolean
    On Error Resume Next
    EstMorphose = (effet = ppEffectMorphByObject Or effet = ppEffectMorphByWord Or effet = ppEffectMorphByChar)
    If Err.Number <> 0 Then EstMorphose = False
    On Error GoTo 0
End Function

Private Function EstDecoratif(nom As String) As Boolean
    EstDecoratif = (nom = "!!etoiles" Or nom = "!!halo" Or nom = "vignette" Or nom = "fond-image" _
                    Or Left$(nom, 4) = "!!av" Or Right$(nom, 6) = "-picto")
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

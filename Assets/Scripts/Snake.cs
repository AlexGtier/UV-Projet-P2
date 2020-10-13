﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Snake : MonoBehaviour
{
    //Sauvegarder les differentes lignes composant la queue
    public Tail queuePrefab;
    private List<Tail> listQueue;
    private Tail currentTail;
    public Color colorTail;
    //determine si on est sur un trou ou si on dessine la queue
    public bool isDrawingTail;
    public Transform positionHotSpotEnd;

    //Generer des trous dans la queue du serpent
    public float minDistanceTail = 450f;
    public float maxDistanceTail = 500f;
    public float distanceBreakInTail = 45f;

    //Pour les collisions
    public Transform positionHotSpotFront;
    public GameObject dieAnimation;
    public float radiusExplosionDeath = 1f;

    //Autres
    private Animator anim;

    void Start()
    {
        anim = gameObject.GetComponent<Animator>();
        isDrawingTail = true;
        listQueue = new List<Tail>();
        StartCoroutine(DrawCurrentTail());
        anim.SetBool("Free", false);
    }


    /*
     * Créer la queue du serpent
     */
    //détermine si on dessine la queue ou si on fait un trou
    private IEnumerator DrawCurrentTail()
    {
        while (true)
        {
            createTail();
            float distanceTail = Random.Range(minDistanceTail, maxDistanceTail);
            yield return new WaitForSeconds(distanceTail);
            isDrawingTail = false;
            gameObject.GetComponent<CapsuleCollider2D>().enabled = false;
            anim.SetBool("Free", true);
            yield return new WaitForSeconds(distanceBreakInTail);
            isDrawingTail = true;
            gameObject.GetComponent<CapsuleCollider2D>().enabled = true;
            anim.SetBool("Free", false);
        }
    }

    void Update()
    {
        //dessine la queue
        if (isDrawingTail)
        {
            currentTail.updateTailVertex(positionHotSpotEnd.position);
        }
    }

    //Crée le bout de queue suivant
    public void createTail()
    {
        currentTail = Instantiate(queuePrefab) as Tail;
        currentTail.SetColor(colorTail);
        listQueue.Add(currentTail);
    }



    /**
     * Collisions
     */
    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Wall"))
        {
            Die();
        }
        else if (collision.CompareTag("Tail"))
        {
            collideTail(collision.GetComponent<Tail>());
            Die();
        }
    }

    void Die()
    {
        GameObject effect = Instantiate(dieAnimation, transform.position, Quaternion.identity);
        Destroy(effect, 0.3f);
        Destroy(gameObject);
    }

    //on crée 2 queues supplémentaires qui vont chacun représenter les moities restantes de la queue
    private void collideTail(Tail collidedTail)
    {
        bool isInImpactArea = false;
        createTail();
        currentTail.SetColor(collidedTail.color);
        for (int i = 0; i < collidedTail.line.positionCount; i++)
        {
            Vector2 currentPoint = collidedTail.line.GetPosition(i);
            if (Vector2.Distance(currentPoint, positionHotSpotFront.position) > radiusExplosionDeath)
            {
                currentTail.updateTailVertex(new Vector3(currentPoint.x, currentPoint.y, -0.1f));
            }
            else if (!isInImpactArea)
            {
                createTail();
                currentTail.SetColor(collidedTail.color);
                isInImpactArea = true;
            }
        }
        collidedTail.gameObject.SetActive(false);
    }
}

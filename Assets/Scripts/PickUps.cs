﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class PickUps : MonoBehaviour
{
    public float speedModif = 0.2f;

    public abstract void ActivatePickUp(GameObject ship);
}

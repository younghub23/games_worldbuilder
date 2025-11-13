# API SPECIFICATION
## Empire Genesis Backend REST API v1

**Base URL:** `https://api.empiregenesis.com/api/v1`
**Dev URL:** `http://localhost:3000/api/v1`

---

## AUTHENTICATION

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### POST /auth/register
Register a new player account.

**Request Body:**
```json
{
  "username": "string (3-20 chars)",
  "email": "string (optional)",
  "apple_id": "string (optional)",
  "google_id": "string (optional)",
  "device_id": "string"
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "player_id": "uuid",
    "username": "string",
    "token": "jwt_token",
    "refresh_token": "refresh_token"
  }
}
```

---

### POST /auth/login
Login with existing account.

**Request Body:**
```json
{
  "apple_id": "string (or google_id or device_id)",
  "device_id": "string"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "user_id": "uuid",
    "player_id": "uuid",
    "username": "string",
    "token": "jwt_token",
    "refresh_token": "refresh_token"
  }
}
```

---

### POST /auth/refresh
Refresh JWT token.

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token",
    "refresh_token": "new_refresh_token"
  }
}
```

---

## PLAYER

### GET /player/profile
Get player profile and game state.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "player_id": "uuid",
    "username": "string",
    "display_name": "string",
    "level": 5,
    "experience": 12500,
    "current_era": 1,
    "population": 127,
    "resources": {
      "gold": 1250000,
      "wood": 8500,
      "stone": 6200,
      "food": 3400,
      "water": 2100,
      "gems": 150,
      "scrolls": 3,
      "prestige_points": 0
    },
    "vip_level": 0,
    "city_beauty_score": 45,
    "alliance": {
      "id": "uuid",
      "name": "string",
      "tag": "string",
      "role": "member"
    },
    "created_at": "2025-01-01T00:00:00Z",
    "last_login": "2025-01-15T12:00:00Z"
  }
}
```

---

### PUT /player/profile
Update player profile.

**Auth:** Required

**Request Body:**
```json
{
  "display_name": "string (optional)",
  "avatar_id": "int (optional)"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "display_name": "new_name",
    "avatar_id": 5
  }
}
```

---

### GET /player/resources
Get current resource amounts.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "gold": 1250000,
    "wood": 8500,
    "stone": 6200,
    "food": 3400,
    "water": 2100,
    "gems": 150,
    "scrolls": 3,
    "prestige_points": 0,
    "storage_capacities": {
      "gold": 10000000,
      "wood": 10000,
      "stone": 10000,
      "food": 5000,
      "water": 5000
    }
  }
}
```

---

## BUILDINGS

### GET /buildings
Get all player buildings.

**Auth:** Required

**Query Parameters:**
- `include_under_construction` (boolean, default: true)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "buildings": [
      {
        "id": "uuid",
        "building_type_id": 1,
        "building_type_name": "Tent",
        "category": "housing",
        "level": 2,
        "position": {
          "x": 10,
          "y": 15
        },
        "is_under_construction": false,
        "construction_finish_at": null,
        "last_collected_at": "2025-01-15T11:30:00Z",
        "production": {
          "type": "population",
          "capacity": 5,
          "current": 5
        },
        "created_at": "2025-01-10T08:00:00Z"
      }
    ],
    "total_count": 15,
    "building_queue_slots": 2,
    "buildings_in_queue": 1
  }
}
```

---

### POST /buildings
Place a new building.

**Auth:** Required

**Request Body:**
```json
{
  "building_type_id": 1,
  "position": {
    "x": 12,
    "y": 18
  },
  "use_speed_up": false
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "building_type_id": 1,
    "level": 1,
    "position": {
      "x": 12,
      "y": 18
    },
    "is_under_construction": true,
    "construction_started_at": "2025-01-15T12:00:00Z",
    "construction_finish_at": "2025-01-15T12:30:00Z",
    "resources_spent": {
      "wood": 10
    }
  }
}
```

**Errors:**
- `400`: Insufficient resources
- `400`: Invalid position (occupied or out of bounds)
- `400`: Building not unlocked for current era
- `400`: Building queue full

---

### PUT /buildings/:id/upgrade
Upgrade a building.

**Auth:** Required

**Request Body:**
```json
{
  "use_speed_up": false
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "level": 2,
    "is_under_construction": true,
    "construction_finish_at": "2025-01-15T14:00:00Z",
    "resources_spent": {
      "wood": 15,
      "stone": 10
    }
  }
}
```

---

### DELETE /buildings/:id
Remove a building.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "resources_refunded": {
      "wood": 5,
      "stone": 3
    }
  }
}
```

---

### POST /buildings/:id/collect
Collect production from a building.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "collected": {
      "wood": 120
    },
    "next_collection_at": "2025-01-15T13:00:00Z"
  }
}
```

---

### POST /buildings/:id/speed-up
Use speed-up item or gems to finish construction instantly.

**Auth:** Required

**Request Body:**
```json
{
  "use_gems": false,
  "speed_up_item_id": "uuid (optional)"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "building_id": "uuid",
    "is_under_construction": false,
    "gems_spent": 0,
    "speed_up_used": true
  }
}
```

---

## HEROES

### GET /heroes
Get all player heroes.

**Auth:** Required

**Query Parameters:**
- `filter` (string: "all" | "equipped" | "unequipped")
- `sort` (string: "rarity" | "level" | "acquired_date")

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "heroes": [
      {
        "id": "uuid",
        "hero_type_id": 1,
        "name": "Aria the Forester",
        "rarity": 4,
        "element": "nature",
        "level": 15,
        "experience": 2500,
        "experience_to_next_level": 3000,
        "is_equipped": true,
        "assigned_building_id": "uuid",
        "abilities": [
          {
            "name": "Master Woodsman",
            "type": "passive",
            "effect": "+20% wood production"
          }
        ],
        "acquired_at": "2025-01-10T08:00:00Z"
      }
    ],
    "total_heroes": 5,
    "max_hero_capacity": 100
  }
}
```

---

### GET /heroes/:id
Get hero details.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "hero_type_id": 1,
    "name": "Aria the Forester",
    "rarity": 4,
    "level": 15,
    "experience": 2500,
    "stats": {
      "base_power": 120,
      "bonus_power": 35
    },
    "abilities": [
      {
        "id": 1,
        "name": "Master Woodsman",
        "type": "passive",
        "level": 3,
        "effect": "+20% wood production",
        "cooldown_hours": null
      }
    ],
    "synergies": [
      {
        "with_hero_id": 2,
        "with_hero_name": "Brock the Mason",
        "bonus": "+5% all resource production"
      }
    ]
  }
}
```

---

### PUT /heroes/:id/level-up
Level up a hero using experience items or resources.

**Auth:** Required

**Request Body:**
```json
{
  "experience_items": [
    {
      "item_id": "uuid",
      "quantity": 5
    }
  ]
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "hero_id": "uuid",
    "old_level": 15,
    "new_level": 18,
    "experience": 500,
    "items_used": 5
  }
}
```

---

### PUT /heroes/:id/assign
Assign hero to a building.

**Auth:** Required

**Request Body:**
```json
{
  "building_id": "uuid"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "hero_id": "uuid",
    "assigned_building_id": "uuid",
    "production_bonus": 0.20
  }
}
```

---

### PUT /heroes/:id/unassign
Remove hero from building.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "hero_id": "uuid",
    "assigned_building_id": null
  }
}
```

---

## GACHA

### GET /gacha/rates
Get current gacha rates and pity information.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "banners": [
      {
        "id": "standard",
        "name": "Standard Hero Banner",
        "type": "hero",
        "rates": {
          "4_star": 0.06,
          "5_star": 0.006,
          "6_star": 0.003
        },
        "pity": {
          "4_star_counter": 3,
          "4_star_guarantee": 10,
          "5_star_counter": 45,
          "5_star_guarantee": 90,
          "6_star_counter": 78,
          "6_star_guarantee": 120
        },
        "cost": {
          "single": {
            "gems": 300,
            "scrolls": 1
          },
          "ten_pull": {
            "gems": 2700,
            "scrolls": 10
          }
        }
      }
    ]
  }
}
```

---

### POST /gacha/pull
Perform a single gacha pull.

**Auth:** Required

**Request Body:**
```json
{
  "banner_id": "standard",
  "currency_type": "gems"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "result_type": "hero",
    "result_id": 5,
    "result_name": "Elena the Architect",
    "rarity": 4,
    "is_new": true,
    "is_pity": false,
    "currency_spent": {
      "gems": 300
    },
    "pity_counters_updated": {
      "4_star": 0,
      "5_star": 46,
      "6_star": 79
    }
  }
}
```

---

### POST /gacha/pull-10
Perform a 10-pull.

**Auth:** Required

**Request Body:**
```json
{
  "banner_id": "standard",
  "currency_type": "scrolls"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "result_type": "hero",
        "result_id": 3,
        "result_name": "Finn the Fisher",
        "rarity": 4,
        "is_new": false
      }
      // ... 9 more results
    ],
    "summary": {
      "4_star_count": 2,
      "5_star_count": 1,
      "6_star_count": 0
    },
    "currency_spent": {
      "scrolls": 10
    },
    "pity_counters_updated": {
      "4_star": 0,
      "5_star": 0,
      "6_star": 89
    }
  }
}
```

---

### GET /gacha/history
Get gacha pull history.

**Auth:** Required

**Query Parameters:**
- `limit` (int, default: 50, max: 100)
- `offset` (int, default: 0)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": "uuid",
        "banner_type": "standard",
        "result_type": "hero",
        "result_name": "Admiral Katrina",
        "rarity": 5,
        "pull_number": 87,
        "was_pity": false,
        "created_at": "2025-01-15T12:00:00Z"
      }
    ],
    "total_pulls": 127,
    "total_count": 127
  }
}
```

---

## ALLIANCE

### GET /alliances
List and search alliances.

**Auth:** Required

**Query Parameters:**
- `search` (string, optional)
- `min_level` (int, optional)
- `has_space` (boolean, optional)
- `limit` (int, default: 20)
- `offset` (int, default: 0)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "alliances": [
      {
        "id": "uuid",
        "name": "Empire Builders",
        "tag": "EB",
        "level": 15,
        "member_count": 38,
        "max_members": 50,
        "description": "Active alliance for serious players",
        "requirements": {
          "min_level": 10,
          "min_era": 2
        },
        "is_recruiting": true
      }
    ],
    "total_count": 1523
  }
}
```

---

### POST /alliances
Create a new alliance.

**Auth:** Required

**Request Body:**
```json
{
  "name": "string (3-50 chars)",
  "tag": "string (2-5 chars)",
  "description": "string (max 500 chars)",
  "requirements": {
    "min_level": 5,
    "min_era": 1
  }
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Empire Builders",
    "tag": "EB",
    "level": 1,
    "leader_id": "uuid",
    "created_at": "2025-01-15T12:00:00Z"
  }
}
```

**Errors:**
- `400`: Already in an alliance
- `409`: Name or tag already taken
- `400`: Insufficient resources (cost: 1000 gold)

---

### GET /alliances/:id
Get alliance details.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "Empire Builders",
    "tag": "EB",
    "level": 15,
    "experience": 125000,
    "description": "Active alliance",
    "member_count": 38,
    "max_members": 50,
    "leader": {
      "player_id": "uuid",
      "username": "Commander",
      "level": 45
    },
    "benefits": {
      "production_bonus": 0.05,
      "warehouse_capacity": 1000000,
      "research_slots": 3
    },
    "created_at": "2024-06-15T10:00:00Z"
  }
}
```

---

### POST /alliances/:id/join
Join an alliance.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "alliance_id": "uuid",
    "player_id": "uuid",
    "role": "member",
    "joined_at": "2025-01-15T12:00:00Z"
  }
}
```

**Errors:**
- `400`: Already in an alliance
- `403`: Does not meet requirements
- `400`: Alliance full

---

### DELETE /alliances/:id/leave
Leave current alliance.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Left alliance successfully"
}
```

---

### GET /alliances/:id/members
Get alliance members.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "members": [
      {
        "player_id": "uuid",
        "username": "Player1",
        "display_name": "The Builder",
        "level": 35,
        "role": "leader",
        "contribution_points": 15000,
        "last_active": "2025-01-15T11:00:00Z",
        "joined_at": "2024-06-15T10:00:00Z"
      }
    ],
    "total_members": 38
  }
}
```

---

### POST /alliances/:id/donate
Donate resources to alliance.

**Auth:** Required

**Request Body:**
```json
{
  "resources": {
    "gold": 10000,
    "wood": 500
  }
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "contribution_points_earned": 115,
    "total_contribution_points": 15115,
    "alliance_experience_gained": 100
  }
}
```

---

## SHOP & IAP

### GET /shop/products
Get available IAP products.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "products": [
      {
        "product_id": "com.empiregenesis.gems100",
        "type": "consumable",
        "name": "Gems Pack - Small",
        "description": "100 Gems",
        "price_usd": 0.99,
        "contents": {
          "gems": 100
        },
        "first_time_bonus": {
          "gems": 500
        }
      },
      {
        "product_id": "com.empiregenesis.seasonpass",
        "type": "subscription",
        "name": "Season Pass",
        "description": "Monthly subscription with exclusive rewards",
        "price_usd": 9.99,
        "duration_days": 30
      }
    ],
    "daily_deals": [
      {
        "deal_id": "uuid",
        "name": "Resource Bundle",
        "price_usd": 1.99,
        "contents": {
          "gold": 50000,
          "wood": 2000,
          "stone": 2000
        },
        "expires_at": "2025-01-16T00:00:00Z"
      }
    ]
  }
}
```

---

### POST /shop/purchase
Verify and process an IAP purchase.

**Auth:** Required

**Request Body:**
```json
{
  "product_id": "com.empiregenesis.gems100",
  "platform": "ios",
  "receipt": "base64_encoded_receipt",
  "transaction_id": "string"
}
```

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "purchase_id": "uuid",
    "product_id": "com.empiregenesis.gems100",
    "is_verified": true,
    "rewards_granted": {
      "gems": 500
    },
    "was_first_purchase": true,
    "vip_points_earned": 1
  }
}
```

---

## TRADE

### POST /trade/create
Create a trade offer.

**Auth:** Required

**Request Body:**
```json
{
  "offering": {
    "wood": 1000
  },
  "requesting": {
    "stone": 800
  },
  "duration_hours": 24
}
```

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "trade_id": "uuid",
    "seller_id": "uuid",
    "offering": {
      "wood": 1000
    },
    "requesting": {
      "stone": 800
    },
    "expires_at": "2025-01-16T12:00:00Z",
    "created_at": "2025-01-15T12:00:00Z"
  }
}
```

---

### GET /trade/offers
Get active trade offers.

**Auth:** Required

**Query Parameters:**
- `resource_type` (string, optional)
- `limit` (int, default: 20)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "offers": [
      {
        "trade_id": "uuid",
        "seller": {
          "player_id": "uuid",
          "username": "Trader Joe"
        },
        "offering": {
          "wood": 1000
        },
        "requesting": {
          "stone": 800
        },
        "expires_at": "2025-01-16T12:00:00Z"
      }
    ]
  }
}
```

---

### POST /trade/:id/accept
Accept a trade offer.

**Auth:** Required

**Response:** `200 OK`
```json
{
  "success": true,
  "data": {
    "trade_id": "uuid",
    "resources_given": {
      "stone": 800
    },
    "resources_received": {
      "wood": 1000
    }
  }
}
```

---

## ANALYTICS

### POST /analytics/event
Track a game event.

**Auth:** Required

**Request Body:**
```json
{
  "event_name": "building_placed",
  "properties": {
    "building_type": "tent",
    "era": 1,
    "position_x": 10,
    "position_y": 15
  },
  "timestamp": "2025-01-15T12:00:00Z"
}
```

**Response:** `202 Accepted`
```json
{
  "success": true,
  "message": "Event tracked"
}
```

---

## ERROR RESPONSES

All errors follow this format:

```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_RESOURCES",
    "message": "Not enough wood to build this structure",
    "details": {
      "required": {
        "wood": 100
      },
      "available": {
        "wood": 50
      }
    }
  }
}
```

**Common Error Codes:**
- `INVALID_REQUEST` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `RATE_LIMIT_EXCEEDED` (429)
- `INTERNAL_SERVER_ERROR` (500)

---

## RATE LIMITING

**Per-endpoint limits:**
- Auth endpoints: 10 requests/minute
- Gacha pulls: 100 requests/hour
- General endpoints: 1000 requests/hour

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1642252800
```

---

## WEBSOCKET EVENTS

**Connection:**
```javascript
const socket = io('wss://api.empiregenesis.com', {
  auth: {
    token: 'jwt_token'
  }
});
```

**Client → Server:**
```javascript
// Building completed
socket.emit('building:completed', { building_id: 'uuid' });

// Alliance chat
socket.emit('alliance:chat', { message: 'Hello!' });
```

**Server → Client:**
```javascript
// Resource update
socket.on('resource:update', (data) => {
  // { gold: 1250500, wood: 8550, ... }
});

// Building completed notification
socket.on('building:completed', (data) => {
  // { building_id: 'uuid', building_type: 'tent' }
});

// Alliance message
socket.on('alliance:message', (data) => {
  // { sender: 'username', message: 'text', timestamp: '...' }
});
```

---

**API Version:** v1.0.0
**Last Updated:** November 2025

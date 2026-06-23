const labTopologies = [
  {
    "name": "DMZ + LAN",
    "nodes": [
      {
        "x": 400,
        "y": 70,
        "label": "Internet",
        "type": "cloud"
      },
      {
        "x": 400,
        "y": 190,
        "label": "Firewall",
        "type": "fw"
      },
      {
        "x": 220,
        "y": 330,
        "label": "Web DMZ",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 330,
        "label": "DNS DMZ",
        "type": "srv"
      },
      {
        "x": 580,
        "y": 330,
        "label": "DB LAN",
        "type": "srv"
      }
    ],
    "links": [
      [
        0,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ],
      [
        1,
        4
      ]
    ]
  },
  {
    "name": "Cloud Híbrida",
    "nodes": [
      {
        "x": 130,
        "y": 210,
        "label": "On-Prem",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 100,
        "label": "Cloud VPC",
        "type": "cloud"
      },
      {
        "x": 650,
        "y": 210,
        "label": "SaaS",
        "type": "cloud"
      }
    ],
    "links": [
      [
        0,
        1
      ],
      [
        1,
        2
      ]
    ]
  },
  {
    "name": "VPN Site-to-Site",
    "nodes": [
      {
        "x": 130,
        "y": 150,
        "label": "Sede A",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 200,
        "label": "Internet VPN",
        "type": "cloud"
      },
      {
        "x": 650,
        "y": 150,
        "label": "Sede B",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 70,
        "label": "HQ",
        "type": "srv"
      }
    ],
    "links": [
      [
        0,
        1
      ],
      [
        1,
        2
      ],
      [
        1,
        3
      ]
    ]
  },
  {
    "name": "Cluster HA",
    "nodes": [
      {
        "x": 400,
        "y": 60,
        "label": "VIP",
        "type": "fw"
      },
      {
        "x": 200,
        "y": 200,
        "label": "Node 1",
        "type": "srv"
      },
      {
        "x": 600,
        "y": 200,
        "label": "Node 2",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 330,
        "label": "Shared Storage",
        "type": "cloud"
      }
    ],
    "links": [
      [
        0,
        1
      ],
      [
        0,
        2
      ],
      [
        1,
        3
      ],
      [
        2,
        3
      ]
    ]
  }
];
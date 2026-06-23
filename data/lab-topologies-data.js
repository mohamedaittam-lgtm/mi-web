var labTopologies = [
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
      },
      {
        "x": 400,
        "y": 260,
        "label": "VPN GW",
        "type": "fw"
      }
    ],
    "links": [
      [
        0,
        3
      ],
      [
        3,
        1
      ],
      [
        1,
        2
      ]
    ]
  },
  {
    "name": "Kubernetes",
    "nodes": [
      {
        "x": 300,
        "y": 100,
        "label": "Master",
        "type": "fw"
      },
      {
        "x": 160,
        "y": 270,
        "label": "Worker 1",
        "type": "srv"
      },
      {
        "x": 380,
        "y": 270,
        "label": "Worker 2",
        "type": "srv"
      },
      {
        "x": 540,
        "y": 270,
        "label": "Worker 3",
        "type": "srv"
      },
      {
        "x": 300,
        "y": 390,
        "label": "etcd",
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
        0,
        3
      ],
      [
        0,
        4
      ]
    ]
  },
  {
    "name": "VPN Site-to-Site",
    "nodes": [
      {
        "x": 150,
        "y": 220,
        "label": "Sede A",
        "type": "srv"
      },
      {
        "x": 650,
        "y": 220,
        "label": "Sede B",
        "type": "srv"
      },
      {
        "x": 400,
        "y": 120,
        "label": "WG GW-A",
        "type": "fw"
      },
      {
        "x": 400,
        "y": 320,
        "label": "WG GW-B",
        "type": "fw"
      }
    ],
    "links": [
      [
        0,
        2
      ],
      [
        2,
        3
      ],
      [
        3,
        1
      ]
    ]
  }
];
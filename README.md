# NBA Player Statistics Dashboard

An interactive web dashboard for analyzing NBA player statistics with a modern dark theme interface.

## 🏀 Features

### Interactive Visualizations
1. **Player Comparison**
   - Radar charts comparing up to 3 players
   - Key statistics visualization (Points, Rebounds, Assists)
   - Interactive legend and tooltips

2. **Points Timeline**
   - Player scoring progression over years
   - Interactive line charts with markers
   - Hover details for specific seasons

3. **Career Journey**
   - Team-by-team career timeline
   - Color-coded team transitions
   - Detailed statistics on hover

4. **College to NBA Pipeline**
   - Top 20 colleges by NBA player count
   - Statistical analysis of college contributions
   - Multiple metrics (Points, Rebounds, Assists)

5. **Position Analysis**
   - Position-based statistical distributions
   - Decade and team filtering
   - Box plots with outlier detection

6. **Team Dynasty Explorer**
   - Sunburst visualization of team success
   - Decade-by-decade analysis
   - Multiple statistical metrics

### Design Features
- Professional dark theme for reduced eye strain
- NBA-themed color scheme (Blue #1d428a, Red #c8102e, Gold #fdb927)
- Responsive layout with card-based design
- Interactive dropdowns and filters
- Basketball-themed emojis and icons

## 📊 Project Structure

```
.
├── README.md
├── requirements.txt
├── nba_dashboard.py           # Main dashboard application
└── PlayerIndex_nba_stats.csv  # NBA statistics dataset
```

## 🚀 Setup and Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd nba-dashboard
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Dashboard**
```bash
python nba_dashboard.py
```

4. **Access the Dashboard**
- Open your web browser
- Navigate to `http://localhost:8050`
- Start exploring NBA statistics!

## 📦 Dependencies

- dash==2.14.2
- pandas==2.1.4
- plotly==5.18.0
- numpy==1.26.2

## 🎨 Theme Customization

The dashboard features a professional dark theme with:
- Dark background (#1a1a1a)
- Card background (#2d2d2d)
- Light text (#ffffff)
- NBA accent colors
- Customizable grid and hover states

## 📈 Data Visualization

The dashboard provides multiple ways to analyze NBA data:
- Player performance comparisons
- Career progression analysis
- College-to-NBA pipeline insights
- Position-based statistical analysis
- Team success visualization

## 🔄 Updates and Maintenance

The dashboard is actively maintained with:
- Regular data updates
- Performance optimizations
- New visualization features
- User experience improvements

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 
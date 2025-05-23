import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
import os
import sys

# Initialize the Dash app with proper server configuration
app = Dash(__name__)
server = app.server  # Expose server variable for gunicorn

# Load data
try:
    # Print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print("Directory contents:")
    print(os.listdir())
    
    # Define possible data directories
    data_dirs = [
        os.path.join(os.getcwd(), 'data'),
        os.path.join(os.getcwd(), 'deploy', 'data'),
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'),
        os.getcwd()
    ]
    
    # Print Python path
    print("Python path:")
    print(sys.path)
    
    # Try to find the CSV file
    csv_path = None
    for data_dir in data_dirs:
        possible_path = os.path.join(data_dir, 'PlayerIndex_nba_stats.csv')
        print(f"Checking {possible_path}")
        if os.path.exists(possible_path):
            csv_path = possible_path
            print(f"Found CSV file at: {csv_path}")
            break
    
    if csv_path is None:
        raise FileNotFoundError(f"Could not find PlayerIndex_nba_stats.csv in any of these locations: {', '.join(data_dirs)}")
    
    # Try to read the file
    print(f"Attempting to read CSV from: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Successfully loaded data with shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
except Exception as e:
    print(f"Error loading data: {str(e)}")
    print(f"Stack trace:", file=sys.stderr)
    import traceback
    traceback.print_exc()
    # Provide a minimal dataset with all required columns
    df = pd.DataFrame({
        'PLAYER_FIRST_NAME': ['Sample'],
        'PLAYER_LAST_NAME': ['Player'],
        'FROM_YEAR': [2000],
        'TO_YEAR': [2001],
        'TEAM_NAME': ['Sample Team'],
        'POSITION': ['G'],
        'COLLEGE': ['Sample College'],
        'PTS': [0],
        'REB': [0],
        'AST': [0]
    })
    print("Using fallback dataset for development/testing")

# Color schemes
NBA_COLORS = {
    'primary': '#1d428a',    # NBA Blue
    'secondary': '#c8102e',  # NBA Red
    'accent': '#fdb927',     # NBA Gold
    'background': '#1a1a1a', # Dark background
    'card_bg': '#2d2d2d',    # Darker card background
    'text': '#ffffff',       # Light text
    'text_secondary': '#cccccc', # Secondary text
    'grid': '#3d3d3d',      # Dark grid lines
    'hover': '#3a3a3a'      # Hover state color
}

# Custom styles
CARD_STYLE = {
    'backgroundColor': NBA_COLORS['card_bg'],
    'borderRadius': '10px',
    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.3)',
    'padding': '20px',
    'marginBottom': '20px',
    'color': NBA_COLORS['text']
}

HEADER_STYLE = {
    'color': NBA_COLORS['accent'],
    'textAlign': 'center',
    'padding': '10px',
    'marginBottom': '10px',
    'fontWeight': 'bold',
    'borderBottom': f'3px solid {NBA_COLORS["primary"]}'
}

# Custom styles for dropdowns
DROPDOWN_STYLE = {
    'backgroundColor': NBA_COLORS['card_bg'],
    'color': NBA_COLORS['text'],
    'border': f'1px solid {NBA_COLORS["primary"]}',
    'borderRadius': '5px',
    'option': {'backgroundColor': NBA_COLORS['card_bg']},
    'selected': {'backgroundColor': NBA_COLORS['primary']},
}

# Ensure correct data types
try:
    df['FROM_YEAR'] = df['FROM_YEAR'].astype(int)
    df['PTS'] = df['PTS'].astype(float)
    df['REB'] = df['REB'].astype(float)
    df['AST'] = df['AST'].astype(float)
except ValueError as e:
    print(f"Data type conversion error: {e}")

# Create player options for dropdowns
player_options = [{'label': f"{row['PLAYER_FIRST_NAME']} {row['PLAYER_LAST_NAME']}", 
                  'value': f"{row['PLAYER_FIRST_NAME']} {row['PLAYER_LAST_NAME']}"} 
                  for index, row in df.iterrows()]

# Create decade options for filtering
min_year = df['FROM_YEAR'].min()
max_year = df['FROM_YEAR'].max()
decade_options = [{'label': f"{decade}s", 'value': decade} 
                 for decade in range(min_year // 10 * 10, (max_year // 10 * 10) + 10, 10)]

# Layout of the dashboard
app.layout = html.Div([
    # Dashboard Header
    html.Div([
        html.H1("🏀 NBA Player Statistics Dashboard", 
                style={
                    'textAlign': 'center',
                    'color': NBA_COLORS['accent'],
                    'fontSize': '2.5em',
                    'fontWeight': 'bold',
                    'padding': '20px',
                    'borderBottom': f'4px solid {NBA_COLORS["primary"]}',
                    'backgroundColor': NBA_COLORS['card_bg'],
                    'marginBottom': '20px',
                    'borderRadius': '10px'
                })
    ]),
    
    # Player Comparison Radar Chart
    html.Div([
        html.H2("Player Comparison", style=HEADER_STYLE),
        html.Div([
            html.I("Compare up to 3 players' key statistics", 
                   style={'color': NBA_COLORS['secondary'], 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='comparison-player-dropdown',
                options=player_options,
                multi=True,
                placeholder="Select up to 3 players",
                style={
                    'width': '100%',
                    'marginBottom': '15px',
                    'color': '#000000',  # Black text for dropdown items
                    'backgroundColor': '#ffffff',  # White background
                }
            ),
        ]),
        dcc.Graph(id='radar-chart', style={'height': '500px'})
    ], style=CARD_STYLE),

    # Points Over Time & Career Arc Explorer (Side by Side)
    html.Div([
        html.Div([
            html.H2("Points Timeline", style=HEADER_STYLE),
            dcc.Dropdown(
                id='player-dropdown',
                options=player_options,
                placeholder="Select a player",
                style={
                    'width': '100%',
                    'marginBottom': '15px',
                    'color': '#000000',
                    'backgroundColor': '#ffffff',
                }
            ),
            dcc.Graph(id='line-chart', style={'height': '500px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', **CARD_STYLE}),
        
        html.Div([
            html.H2("Career Journey", style=HEADER_STYLE),
            dcc.Dropdown(
                id='career-player-dropdown',
                options=player_options,
                placeholder="Select a player",
                style={
                    'width': '100%',
                    'marginBottom': '15px',
                    'color': '#000000',
                    'backgroundColor': '#ffffff',
                }
            ),
            dcc.Graph(id='career-arc-timeline', style={'height': '500px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', **CARD_STYLE}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

    # Team Legacy Graph
    html.Div([
        html.H2("Team Dynasty Explorer", style=HEADER_STYLE),
        html.I("Explore team success across different eras", 
               style={'color': NBA_COLORS['secondary'], 'marginBottom': '10px'}),
        dcc.Dropdown(
            id='legacy-metric-dropdown',
            options=[
                {'label': '🏀 Points', 'value': 'PTS'},
                {'label': '🔄 Rebounds', 'value': 'REB'},
                {'label': '👥 Assists', 'value': 'AST'}
            ],
            value='PTS',
            style=DROPDOWN_STYLE
        ),
        dcc.Graph(id='team-legacy-graph', style={'height': '800px'})
    ], style=CARD_STYLE),

    # College Pipeline & Position Distribution (Side by Side)
    html.Div([
        html.Div([
            html.H2("College to NBA Pipeline", style=HEADER_STYLE),
            dcc.Dropdown(
                id='college-metric-dropdown',
                options=[
                    {'label': '👥 Number of Players', 'value': 'count'},
                    {'label': '🏀 Average Points', 'value': 'PTS'},
                    {'label': '🔄 Average Rebounds', 'value': 'REB'},
                    {'label': '👥 Average Assists', 'value': 'AST'}
                ],
                value='count',
                style={
                    'width': '100%',
                    'marginBottom': '15px',
                    'color': '#000000',
                    'backgroundColor': '#ffffff',
                }
            ),
            dcc.Graph(id='college-pipeline-chart', style={'height': '500px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', **CARD_STYLE}),
        
        html.Div([
            html.H2("Position Analysis", style=HEADER_STYLE),
            html.Div([
                dcc.Dropdown(
                    id='position-stat-dropdown',
                    options=[
                        {'label': '🏀 Points', 'value': 'PTS'},
                        {'label': '🔄 Rebounds', 'value': 'REB'},
                        {'label': '👥 Assists', 'value': 'AST'}
                    ],
                    value='PTS',
                    style={
                        'width': '32%',
                        'marginRight': '2%',
                        'color': '#000000',
                        'backgroundColor': '#ffffff',
                    }
                ),
                dcc.Dropdown(
                    id='position-decade-dropdown',
                    options=decade_options,
                    placeholder="Select decade",
                    style={
                        'width': '32%',
                        'marginRight': '2%',
                        'color': '#000000',
                        'backgroundColor': '#ffffff',
                    }
                ),
                dcc.Dropdown(
                    id='position-team-dropdown',
                    options=[{'label': team, 'value': team} for team in sorted(df['TEAM_NAME'].unique())],
                    placeholder="Select team",
                    style={
                        'width': '32%',
                        'color': '#000000',
                        'backgroundColor': '#ffffff',
                    }
                )
            ], style={'display': 'flex', 'marginBottom': '15px'}),
            dcc.Graph(id='position-distribution-chart', style={'height': '500px'})
        ], style={'width': '49%', 'display': 'inline-block', 'verticalAlign': 'top', **CARD_STYLE}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

], style={
    'fontFamily': '"Helvetica Neue", Helvetica, Arial, sans-serif',
    'backgroundColor': NBA_COLORS['background'],
    'padding': '20px',
    'minHeight': '100vh',
    'color': NBA_COLORS['text']
})

# Callback for updating the radar chart
@app.callback(
    Output('radar-chart', 'figure'),
    [Input('comparison-player-dropdown', 'value')]
)
def update_radar_chart(selected_players):
    if not selected_players or len(selected_players) > 3:
        return go.Figure()
    
    radar_data = []
    for player in selected_players:
        first_name, last_name = player.split()
        player_data = df[(df['PLAYER_FIRST_NAME'] == first_name) & (df['PLAYER_LAST_NAME'] == last_name)]
        if not player_data.empty:
            avg_stats = player_data[['PTS', 'REB', 'AST']].mean()
            radar_data.append(go.Scatterpolar(
                r=[avg_stats['PTS'], avg_stats['REB'], avg_stats['AST']],
                theta=['Points', 'Rebounds', 'Assists'],
                fill='toself',
                name=player,
                line_color=px.colors.qualitative.Set3[len(radar_data)]
            ))
    
    fig = go.Figure(data=radar_data)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor=NBA_COLORS['grid'],
                color=NBA_COLORS['text']
            ),
            bgcolor=NBA_COLORS['card_bg'],
            angularaxis=dict(
                color=NBA_COLORS['text']
            )
        ),
        showlegend=True,
        paper_bgcolor=NBA_COLORS['card_bg'],
        plot_bgcolor=NBA_COLORS['card_bg'],
        font=dict(color=NBA_COLORS['text']),
        title={
            'text': 'Player Comparison',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': NBA_COLORS['accent']}
        }
    )
    return fig

# Callback for updating the line chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('player-dropdown', 'value')]
)
def update_line_chart(selected_player):
    if selected_player is None:
        return go.Figure()
    
    first_name, last_name = selected_player.split()
    player_data = df[(df['PLAYER_FIRST_NAME'] == first_name) & (df['PLAYER_LAST_NAME'] == last_name)]
    
    if player_data.empty:
        return go.Figure()
    
    fig = px.line(player_data, x='FROM_YEAR', y='PTS', title=f'{selected_player} Points Over Time', markers=True)
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(
        paper_bgcolor=NBA_COLORS['card_bg'],
        plot_bgcolor=NBA_COLORS['card_bg'],
        font=dict(color=NBA_COLORS['text']),
        xaxis=dict(gridcolor=NBA_COLORS['grid'], color=NBA_COLORS['text']),
        yaxis=dict(gridcolor=NBA_COLORS['grid'], color=NBA_COLORS['text'])
    )
    return fig

# Callback for updating the career arc timeline
@app.callback(
    Output('career-arc-timeline', 'figure'),
    [Input('career-player-dropdown', 'value')]
)
def update_career_arc(selected_player):
    if selected_player is None:
        return go.Figure()
    
    first_name, last_name = selected_player.split()
    player_data = df[(df['PLAYER_FIRST_NAME'] == first_name) & (df['PLAYER_LAST_NAME'] == last_name)]
    
    if player_data.empty:
        return go.Figure()
    
    fig = px.timeline(player_data, x_start='FROM_YEAR', x_end='TO_YEAR', y='TEAM_NAME', color='TEAM_NAME',
                     hover_data={'PTS': True, 'REB': True, 'AST': True}, title=f'{selected_player} Career Arc')
    fig.update_layout(
        paper_bgcolor=NBA_COLORS['card_bg'],
        plot_bgcolor=NBA_COLORS['card_bg'],
        font=dict(color=NBA_COLORS['text']),
        xaxis=dict(gridcolor=NBA_COLORS['grid'], color=NBA_COLORS['text']),
        yaxis=dict(gridcolor=NBA_COLORS['grid'], color=NBA_COLORS['text'])
    )
    return fig

# New callback for College Pipeline Analyzer
@app.callback(
    Output('college-pipeline-chart', 'figure'),
    [Input('college-metric-dropdown', 'value')]
)
def update_college_pipeline(selected_metric):
    try:
        # Create empty figure as fallback
        fig = go.Figure()
        
        # Filter out missing or empty college values
        filtered_df = df[df['COLLEGE'].notna() & (df['COLLEGE'] != '')]
        
        if filtered_df.empty:
            fig.add_annotation(
                text="No college data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False
            )
            return fig
        
        if selected_metric == 'count':
            # Count number of players per college
            college_stats = filtered_df['COLLEGE'].value_counts().nlargest(20)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(college_stats.index),
                    y=list(college_stats.values),
                    text=list(college_stats.values),
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title='Top 20 Colleges by Number of NBA Players',
                xaxis_title='College',
                yaxis_title='Number of Players',
                xaxis_tickangle=-45,
                height=600,
                margin=dict(b=150),  # Increase bottom margin for rotated labels
                showlegend=False
            )
            
        else:
            # Calculate stats only for colleges with at least 5 players
            college_counts = filtered_df['COLLEGE'].value_counts()
            valid_colleges = college_counts[college_counts >= 5].index
            
            if len(valid_colleges) == 0:
                fig.add_annotation(
                    text="No colleges with sufficient data found",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    showarrow=False
                )
                return fig
            
            # Calculate mean stats for valid colleges
            stats_df = (filtered_df[filtered_df['COLLEGE'].isin(valid_colleges)]
                       .groupby('COLLEGE')
                       .agg({
                           selected_metric: 'mean',
                           'PLAYER_LAST_NAME': 'count'  # Count of players
                       })
                       .round(2)
                       .sort_values(selected_metric, ascending=False)
                       .head(20))
            
            fig = go.Figure(data=[
                go.Bar(
                    x=list(stats_df.index),
                    y=list(stats_df[selected_metric]),
                    text=[f"{val:.1f}<br>({count} players)" 
                          for val, count in zip(stats_df[selected_metric], 
                                              stats_df['PLAYER_LAST_NAME'])],
                    textposition='auto',
                    hovertemplate="College: %{x}<br>" +
                                 f"{selected_metric}: %{{y:.1f}}<br>" +
                                 "Players: %{text}<extra></extra>"
                )
            ])
            
            fig.update_layout(
                title=f'Top 20 Colleges by Average {selected_metric}',
                xaxis_title='College',
                yaxis_title=f'Average {selected_metric}',
                xaxis_tickangle=-45,
                height=600,
                margin=dict(b=150),  # Increase bottom margin for rotated labels
                showlegend=False
            )
        
        # Common layout updates
        fig.update_layout(
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(0,0,0,0.1)',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='rgba(0,0,0,0.2)'
            )
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in college pipeline callback: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error generating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        return fig

# New callback for Position-Based Distributions
@app.callback(
    Output('position-distribution-chart', 'figure'),
    [Input('position-stat-dropdown', 'value'),
     Input('position-decade-dropdown', 'value'),
     Input('position-team-dropdown', 'value')]
)
def update_position_distribution(selected_stat, selected_decade, selected_team):
    # Start with a copy of the dataframe
    filtered_df = df.copy()
    
    # Filter out rows with missing positions or selected stat
    filtered_df = filtered_df[
        filtered_df['POSITION'].notna() &
        (filtered_df['POSITION'] != '') &
        filtered_df[selected_stat].notna()
    ]
    
    # Standardize position format (take first letter if multiple positions)
    filtered_df['POSITION'] = filtered_df['POSITION'].str.split('-').str[0]
    
    if selected_decade:
        filtered_df = filtered_df[
            (filtered_df['FROM_YEAR'] >= selected_decade) &
            (filtered_df['FROM_YEAR'] < selected_decade + 10)
        ]
    
    if selected_team:
        filtered_df = filtered_df[filtered_df['TEAM_NAME'] == selected_team]
    
    # Check if we have any data after filtering
    if filtered_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title='No data available for the selected filters',
            annotations=[{
                'text': 'No data available for the selected filters',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig
    
    fig = go.Figure()
    
    # Get unique positions and sort them in a logical order
    position_order = ['G', 'F', 'C', 'G-F', 'F-C']
    positions = sorted(filtered_df['POSITION'].unique(), key=lambda x: (
        position_order.index(x) if x in position_order else len(position_order)
    ))
    
    for pos in positions:
        pos_data = filtered_df[filtered_df['POSITION'] == pos][selected_stat]
        if not pos_data.empty:
            fig.add_trace(go.Box(
                y=pos_data,
                name=pos,
                boxpoints='outliers',
                jitter=0.3,
                pointpos=-1.8
            ))
    
    title = f'{selected_stat} Distribution by Position'
    if selected_decade:
        title += f' ({selected_decade}s)'
    if selected_team:
        title += f' - {selected_team}'
    
    fig.update_layout(
        title=title,
        yaxis_title=selected_stat,
        showlegend=False,
        height=600,
        boxmode='group',
        yaxis=dict(
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickformat='.1f'
        ),
        plot_bgcolor='white'
    )
    
    return fig

# New callback for Team Legacy Graph
@app.callback(
    Output('team-legacy-graph', 'figure'),
    [Input('legacy-metric-dropdown', 'value')]
)
def update_team_legacy(selected_metric):
    try:
        # Create a copy of the dataframe
        legacy_df = df.copy()
        
        # Create decade column
        legacy_df['Decade'] = (legacy_df['FROM_YEAR'] // 10 * 10).astype(str) + 's'
        
        # Calculate team stats by decade
        team_stats = (legacy_df.groupby(['TEAM_NAME', 'Decade'])[selected_metric]
                     .agg(['mean', 'count', 'sum'])
                     .round(2)
                     .reset_index())
        
        # Calculate total team stats
        total_stats = (legacy_df.groupby('TEAM_NAME')[selected_metric]
                      .agg(['mean', 'count', 'sum'])
                      .round(2)
                      .reset_index())
        
        # Prepare data for sunburst chart
        sunburst_data = []
        
        # Add root level (all teams)
        sunburst_data.append({
            'id': 'All Teams',
            'parent': '',
            'value': total_stats['sum'].sum(),
            'name': 'All Teams'
        })
        
        # Add team level
        for _, team_row in total_stats.iterrows():
            team_name = team_row['TEAM_NAME']
            sunburst_data.append({
                'id': team_name,
                'parent': 'All Teams',
                'value': team_row['sum'],
                'name': f"{team_name}<br>Total {selected_metric}: {team_row['sum']:,.0f}<br>"
                       f"Avg {selected_metric}: {team_row['mean']:.1f}<br>"
                       f"Players: {team_row['count']}"
            })
        
        # Add decade level
        for _, decade_row in team_stats.iterrows():
            team_name = decade_row['TEAM_NAME']
            decade = decade_row['Decade']
            decade_id = f"{team_name}_{decade}"
            sunburst_data.append({
                'id': decade_id,
                'parent': team_name,
                'value': decade_row['sum'],
                'name': f"{decade}<br>Total {selected_metric}: {decade_row['sum']:,.0f}<br>"
                       f"Avg {selected_metric}: {decade_row['mean']:.1f}<br>"
                       f"Players: {decade_row['count']}"
            })
        
        # Create sunburst chart
        fig = go.Figure(go.Sunburst(
            ids=[item['id'] for item in sunburst_data],
            labels=[item['name'] for item in sunburst_data],
            parents=[item['parent'] for item in sunburst_data],
            values=[item['value'] for item in sunburst_data],
            branchvalues='total',
            maxdepth=2
        ))
        
        # Update layout
        fig.update_layout(
            title=f'Team Legacy: {selected_metric} Across Decades',
            width=1000,
            height=800,
            sunburstcolorway=px.colors.qualitative.Set3,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error in team legacy callback: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error generating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        return fig

if __name__ == '__main__':
    # Get port from environment variable or default to 8050
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False) 
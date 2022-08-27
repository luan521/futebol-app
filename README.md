# futebol-app
api that provides information about football matches and odds on the site dafabet

Setup
-

- Set environment variables:
    - dafabet_user: dafabet user
    - dafabet_password: dafabet password
    - path_logs_cafu: local path to save logs
    - path_dir_results: local path to save test results

Next steps
-
    - Include code cafu.utils.queries.find_jogo_id:find_jogo_id
    - Create flask api
    - Correct error on function queries.odds.GetOdds.open_odds (log in 22/08/2022 08:39:08 PM): the error occurs when the script is run over a match in progress.
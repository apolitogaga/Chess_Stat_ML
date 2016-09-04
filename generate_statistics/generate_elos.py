__author__ = "codingMonkey"
__project__ = "ChessML"


def elos_to_csv():
    file_num = read_pieces.getNewFileToProcess(STATS_PATH + "elo/", "ELO", '.csv')

    file_write = get_out_file(file_num, STATS_PATH + "elo/", '.csv', "ELO")
    f = open(file_write, "w")
    file_read = getJsonFile(file_num, PATH_OUTPUT_JSON, PAT_OUT)

    print "Processing " + file_read
    data = read_json.get_data(file_read)
    text = ""
    for d in data[:]:
        try:
            # add_competitor(d)
            # add_competitor(d,"White","WhiteElo")
            white = d["white"]
            black = d["black"]
            white_elo = d["white_elo"]
            black_elo = d["black_elo"]
            white_avg_elo = d["white_avg_elo"]
            black_avg_elo = d["black_avg_elo"]
            white_elo = int(white_elo)
            black_elo = int(black_elo)
            res = d["result"]
            len_match = len(d["fen"])
            # l= [white,black,white_elo,black_elo,white_avg_elo,black_avg_elo]
            text += white + "," + black + "," + str(white_elo) + "," + str(black_elo) + "," + str(
                white_avg_elo) + "," + str(black_avg_elo) + "," + str(res) + "," + str(len_match) + linesep
            # print text
        except Exception as e:
            # print e
            pass
            # print "skipping " + str(e)
            # except KeyError as e:
            #     f.close()
            #     remove(file_write)
            #     print e
            #     return -1

            # for val in games.itervalues():
            # json.dump(val.as_dict(), f, encoding='utf-8')
    f.write(text.encode("utf8"))
    f.close()

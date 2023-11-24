/* This file is listing.h
   Copyright (C) 1987-2021 Free Software Foundation, Inc.

   This file is part of GAS, the GNU Assembler.

   GAS is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   GAS is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with GAS; see the file COPYING.  If not, write to the Free
   Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
   02110-1301, USA.  */

#ifndef __listing_h__
#define __listing_h__

#define LISTING_LISTING    1
#define LISTING_SYMBOLS    2
#define LISTING_NOFORM     4
#define LISTING_HLL        8
#define LISTING_NODEBUG   16
#define LISTING_NOCOND    32
#define LISTING_MACEXP    64
#define LISTING_GENERAL  128
#define LISTING_DYN      256  /// xie: 我们追加一种listing的设置，以将listing的单位从物理line变为read_source读取时的line！！！

#define LISTING_DEFAULT    (LISTING_LISTING | LISTING_HLL | LISTING_SYMBOLS)

#ifndef NO_LISTING
#define LISTING_NEWLINE() { if (listing) listing_newline (NULL); }
#else
#define LISTING_NEWLINE() {;}
#endif
#define LISTING_EOF()     LISTING_NEWLINE()

#define LISTING_SKIP_COND() ((listing & LISTING_NOCOND) != 0)

/// xie: 这几个structure原本只写在listing.c中，也只在listing.c的函数中使用，因此没有导出到外面。
/// 但我们需要在外面用listing_info_type，所以将其拷贝到listing.h中。
/* This structure remembers which .s were used.  */
typedef struct file_info_struct
{
    struct file_info_struct * next;
    char *                    filename;
    long                      pos;
    unsigned int              linenum;
    int                       at_end;
} file_info_type;

enum edict_enum
{
    EDICT_NONE,
    EDICT_SBTTL,
    EDICT_TITLE,
    EDICT_NOLIST,
    EDICT_LIST,
    EDICT_NOLIST_NEXT,
    EDICT_EJECT
};


struct list_message
{
    char *message;
    struct list_message *next;
};

/* This structure remembers which line from which file goes into which
   frag.  */
struct list_info_struct
{
    /* Frag which this line of source is nearest to.  */
    fragS *frag; /// 该行对应的frag

    /* The actual line in the source file.  */
    unsigned int line;  /// 对应的源文件行号
    unsigned int dyn_line;  /// xie: 读取时的动态行号

    /* Pointer to the file info struct for the file which this line
       belongs to.  */
    file_info_type *file;

    /* The expanded text of any macro that may have been executing.  */
    char *line_contents;

    /* Next in list.  */
    struct list_info_struct *next;

    /* Pointer to the file info struct for the high level language
       source line that belongs here.  */
    file_info_type *hll_file;

    /* High level language source line.  */
    unsigned int hll_line;

    /* Pointers to linked list of messages associated with this line.  */
    struct list_message *messages, *last_message;

    enum edict_enum edict;
    char *edict_arg;

    /* Nonzero if this line is to be omitted because it contains
       debugging information.  This can become a flags field if we come
       up with more information to store here.  */
    int debugging;
};

typedef struct list_info_struct list_info_type;


void listing_eject (int);
void listing_error (const char *message);
void listing_file (const char *name);
void listing_list (int on);
struct list_info_struct* listing_newline (char *ps);
void listing_prev_line (void);
void listing_print (char *, char **);
void listing_psize (int);
void listing_nopage (int);
void listing_source_file (const char *);
void listing_source_line (unsigned int);
void listing_title (int depth);
void listing_warning (const char *message);
void listing_width (unsigned int x);

extern int listing_lhs_width;
extern int listing_lhs_width_second;
extern int listing_lhs_cont_lines;
extern int listing_rhs_width;

#endif /* __listing_h__ */

/* end of listing.h */
